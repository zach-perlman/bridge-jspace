"""x0_parts (Dan's audit item 2, 24 Oct ~19:30; descriptive, added after data): is recall's loss the bridge word, the
J++ part beyond the word, or any direction aligned with the layer?

On the single-change items (x0_single_*: the asked pick becomes another person's pick), at the model's X0 layer,
Δ = h_alt - h_org at the bridge's word, and four parts of Δ, each removed against a random-subspace part of its own
share (X0's rand_sub), both readers on the identical patch, X0's top-token read:
  w    word only: the least-squares fit of Δ on the J++ directions of the org and alt bridge tokens and their one-token
       surface variants (with / without a leading space, capitalised, upper case, plural);
  jw   J++ without the word: signed OMP, k = 25, over the J++ letter atoms with those variants banned;
  pca  a model-aligned dictionary that is not the lens: the top N_PCA principal directions of the layer's residuals
       over every token of N_HELD held-out prompts (d1_topics_v4, chat, the lookup's prompt), signed OMP, k = 25;
  jpp  X0's J++ part (k = 25), for reference.
Rows are X0's outcome rows (dict w / jw / pca / jpp), so X0's cells (Jdep, Rdep, excess, CIs over bridge entities)
apply. The run also saves h_org, Δ and each part (fp16) for the probe readouts (Dan's item 4).
Reading (Dan): recall's loss mostly in w -> the word; mostly in jw with pca inert -> J++ beyond the word; pca about as
large as J++ -> "J++-specific" means "aligned with the layer's geometry".

uv run python scripts/x0_parts.py run --name x0_parts_27b --single x0_single_27b_r2      # GPU, then the verdict
uv run python scripts/x0_parts.py verdict --name x0_parts_27b                             # CPU
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x0_parts"
RESULTS = pins.RESULTS_DIR / EXP
PARTS = ("w", "jw", "pca", "jpp")
K = 25
N_PCA, N_HELD, HELD_SET, HELD_SEED = 2000, 200, "d1_topics_v4", 0
NOTE = "Descriptive, added after data (Dan's audit, 24 Oct ~19:30, item 2); not part of X0's rule."


def variants(word: str) -> list[str]:
    """The surface forms whose one-token J++ directions make up the word part."""
    forms = {word, word.capitalize(), word.upper(), word + "s", word.capitalize() + "s"}
    return sorted({p + f for f in forms for p in ("", " ")})


def variant_ids(tok, words: list[str]) -> list[int]:
    """The ids of the one-token surface variants of the words."""
    ids = set()
    for w in words:
        for v in variants(w):
            enc = tok.encode(v, add_special_tokens=False)
            if len(enc) == 1:
                ids.add(enc[0])
    return sorted(ids)


def pca_dictionary(model, layer: int) -> tuple[object, dict]:
    """[N_PCA, d] unit rows: the top principal directions of the layer's residuals over every token of N_HELD
    chat-rendered lookup prompts of a fresh set (fixed seed), and the variance share they hold."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import tasks_v2 as T

    items = [it for it in T.load(HELD_SET) if it["word"] == X.LOOKUP]
    picked = random.Random(HELD_SEED).sample(items, N_HELD)
    rows = []
    with torch.no_grad():
        for it in progress(picked, f"residuals at layer {layer} (held-out prompt)"):
            ids = model.tokenizer(T.render(model.tokenizer, it), add_special_tokens=False)["input_ids"]
            rows.append(model.run(torch.tensor([ids], device="cuda"), record=(layer,))[1][layer].float())
        h = torch.cat(rows)
        h = h - h.mean(0)
        evals, evecs = torch.linalg.eigh((h.T @ h).double() / len(h))
        top = evecs[:, -N_PCA:].T.float().contiguous()  # [N_PCA, d], unit rows
    share = float(evals[-N_PCA:].sum() / evals.sum())
    return top, {
        "set": HELD_SET,
        "prompts": N_HELD,
        "tokens": len(h),
        "seed": HELD_SEED,
        "n": N_PCA,
        "variance_share": share,
    }


def stage_run(name: str, single: str, x0b: str | None = None) -> Path:
    """The single-change run's items (all four parts), or with x0b an X0b run's eligible items (w, jw, jpp: Dan's
    item 6, the X0b arms)."""
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows, signed_omp

    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    from scripts import x0b_generalize as B

    src_dir = B.RESULTS / x0b if x0b else X.RESULTS / single
    sm = json.loads((src_dir / "manifest.json").read_text())
    assert x0b or sm["alt"] == "single", f"{single} is not a single-change run"
    used = ("w", "jw", "jpp") if x0b else PARTS
    layer = sm["predicted"]
    scenes = sorted({r["scene"] for r in X.read_jsonl(src_dir / "outcomes.jsonl") if r["rendering"] == "chat"})
    X.ALT = "single"
    model = load_model()
    lens = JLens(model, "jpp")
    tok = model.tokenizer
    cases, _ = B.build_cases(tok, sm["set"]) if x0b else X.build_cases(tok, sm["set"])
    by_scene = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    cases = [by_scene[s] for s in scenes]
    pca, pca_info = pca_dictionary(model, layer) if "pca" in used else (None, None)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "single": x0b or single, "source_exp": "x0b_generalize" if x0b else X.EXP, "single_code": sm["code"],
         "set": sm["set"], "layer": layer, "items": len(scenes), "k": K, "parts": list(used), "pca": pca_info, "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(),
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED, "held_out": HELD_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(json.dumps(pca_info), flush=True)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    letters = model.letter_token_ids()
    row_of = {int(t): i for i, t in enumerate(letters.tolist())}
    jdic = lens.vectors(layer, letters)
    with torch.no_grad():
        h_org, deltas = [], []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {
                v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]]
                for v in ("org", "alt")
            }
            h_org.append(h["org"].float())
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        parts = {"jpp": X.fit(jdic, x, K, "signed")}
        if pca is not None:
            parts["pca"] = X.fit(pca, x, K, "signed")
        w_part, jw_part, n_var = torch.zeros_like(x), torch.zeros_like(x), []
        for i, c in enumerate(progress(cases, "word and J++-without-word parts (case)")):
            ban = variant_ids(tok, [c["bridge"], c["cf_bridge"]])
            n_var.append(len(ban))
            v = lens.vectors(layer, torch.tensor(ban, device="cuda"))  # [m, d] unit
            coef = torch.linalg.lstsq(v.T, x[i][:, None]).solution[:, 0]
            w_part[i] = coef @ v
            keep = torch.ones(len(letters), dtype=torch.bool, device="cuda")
            keep[[row_of[b] for b in ban if b in row_of]] = False
            jw_part[i] = signed_omp(jdic[keep], x[i : i + 1], K)[0]
        parts.update({"w": w_part, "jw": jw_part})
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        arms, shares = {X.WHOLE: x}, []
        for d in used:
            share = parts[d].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            rand = SP.random_subspace_part(x, share, basis)
            fit = "lsq" if d == "w" else "signed"
            k = 0 if d == "w" else K
            arms[(d, k, fit, "no_part")] = x - parts[d]
            arms[(d, k, fit, "no_rand")] = x - rand
            shares += [{"scene": c["scene"], "dict": d, "k": k, "omp": fit, "share": round(float(share[i]), 5),
                        **({"variants": n_var[i]} if d == "w" else {})} for i, c in enumerate(cases)]  # fmt: skip
        keys = list(arms)
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[key][i : i + 1], [c["pos"]])} for key in keys]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                base = {"scene": c["scene"], "domain": c["domain"], "entity": c["bridge"], "rendering": "chat",
                        "layer": layer, "reader": w, "upstream": c["upstream"]}  # fmt: skip
                for key, lg in zip([("-", 0, "-", "none"), *keys], logits, strict=True):
                    d_, k_, fit_, arm = key
                    rows.append({**base, "dict": d_, "k": k_, "omp": fit_, "arm": arm, **X.read_row(lg, rd, digits)})
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "shares.jsonl", shares)
    f16 = lambda t: t.cpu().numpy().astype(np.float16)  # noqa: E731
    np.savez_compressed(out / "states.npz", scene=np.array(scenes), h_org=f16(torch.stack(h_org)), delta=f16(x),
                        **{f"part_{d}": f16(parts[d]) for d in used})  # fmt: skip
    print("wrote", out, flush=True)
    return out


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    shares = X.read_jsonl(src / "shares.jsonl")
    cells = X.cells_of(rows, n_boot)
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    used = m["parts"]
    med = {d: statistics.median(s["share"] for s in shares if s["dict"] == d) for d in used}
    nvar = [s["variants"] for s in shares if s["dict"] == "w"]
    label = {"w": "word only (least squares)", "jw": "J++ without the word (k = 25)", "pca": f"PCA top {N_PCA} (k = 25)",
             "jpp": "J++ (k = 25, reference)"}  # fmt: skip
    lines = [f"# Word, J++ without the word, PCA: {name}", "",
             f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, the single-change items of {m['single']} (n = "
             f"{m['items']}); each part removed against a random subspace of its own share; bootstrap over bridge entities "
             f"({n_boot} resamples). Word variants per item: median {statistics.median(nvar)} (range {min(nvar)}-{max(nvar)}). "
             + (f"PCA: {m['pca']['prompts']} held-out prompts of {m['pca']['set']} ({m['pca']['tokens']} tokens), the top "
                f"{m['pca']['n']} directions hold {m['pca']['variance_share']:.3f} of the residual variance. " if m["pca"] else "")
             + "UNVERIFIED.", "",
             "| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for d in used:
        for w in X.READERS:
            key = next(k for k in cells if k[2] == w and k[3] == d)
            c = cells[key]
            blob.append({"part": d, "reader": w, "median_share": med[d], **c})
            lines.append(f"| {label[d]} | {'lookup' if w == X.LOOKUP else 'recall'} | {med[d]:.3f} | {c['S_whole'][0]:.2f} | "
                         f"{c['S_no_part'][0]:.2f} | {c['S_no_rand'][0]:.2f} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | "
                         f"{X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
    lines += ["", "Reading (Dan, before the run): recall's loss mostly in the word part -> the word; mostly in J++ without the "
              "word with PCA inert -> J++ beyond the word; PCA about as large as J++ -> 'J++-specific' means 'aligned with "
              "the layer's geometry'."]  # fmt: skip
    (out / "verdict.json").write_text(json.dumps({"run": name, "manifest": m, "rows": blob}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--single", default="x0_single_27b_r2")
    ap.add_argument("--x0b", default=None, help="run: an X0b run's eligible items instead (parts w, jw, jpp)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, a.single, a.x0b)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
