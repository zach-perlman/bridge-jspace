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
  jpp  X0's J++ part (k = 25), for reference;
  pca_eq  (Dan, 24 Oct ~21:50, opt-in with --parts) the pca dictionary at J++'s share: k chosen per item so that the
       part's share of ||Δ||² is closest to that item's jpp share (signed OMP on orthonormal atoms takes them in order
       of |coefficient|, so this is exact; checked against signed OMP at k = 25 on every run);
  jwo  (Dan, ~22:05, opt-in with --parts) word-orthogonal jw: signed OMP, k = 25, fit on Δ - w over the J++ letter atoms
       (variants banned) projected off the word's span and renormalised, so it holds none of the word's energy (checked
       per item); removing it leaves the word part intact.
Rows are X0's outcome rows (dict w / jw / pca / jpp / pca_eq / jwo), so X0's cells (Jdep, Rdep, excess, CIs over bridge
entities) apply. The run also saves h_org, Δ and each part (fp16) for the probe readouts (Dan's item 4).
Reading (Dan): recall's loss mostly in w -> the word; mostly in jw with pca inert -> J++ beyond the word; pca about as
large as J++ -> "J++-specific" means "aligned with the layer's geometry". pca_eq (Dan, ~21:50): recall-specific like
J++ -> "J++-specific" means "aligned with the layer's main directions"; hurts both -> J++ is the only dictionary that
separates the readers; inert -> J++ is special at equal share. jwo (Dan, ~22:05): recall still loses >= 0.20 with the
word intact -> "recall needs J++ components beyond the word"; <= 0.10 -> "the word and the other J++ components are
redundant: either suffices".

uv run python scripts/x0_parts.py run --name x0_parts_27b --single x0_single_27b_r2      # GPU, then the verdict
uv run python scripts/x0_parts.py run --name x0_pcaeq_27b --single x0_single_27b_r2 --parts pca_eq,jwo,jpp
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


def equal_share(top, x, target):
    """The part of each row of x [n, d] over the orthonormal rows of top, taken in order of |coefficient| (signed OMP's
    order on orthonormal atoms), with k per row so that its share of the row's ||x||² is closest to target[row].
    Returns (parts [n, d], k [n])."""
    import torch

    coef = x @ top.T  # [n, N_PCA]
    order = coef.abs().argsort(dim=-1, descending=True)
    c = coef.gather(-1, order)
    cum = torch.cumsum(c**2, dim=-1) / (x.norm(dim=-1, keepdim=True) ** 2).clamp_min(1e-30)
    cum = torch.cat([torch.zeros_like(cum[:, :1]), cum], dim=-1)  # [n, N_PCA + 1]: the share of the first k atoms
    k = (cum - target.float()[:, None]).abs().argmin(dim=-1)
    c = c * (torch.arange(c.shape[1], device=x.device)[None, :] < k[:, None])
    return torch.zeros_like(coef).scatter(-1, order, c) @ top, k


def word_parts(lens, tok, layer: int, letters, jdic, cases: list[dict], x, want: set[str]) -> tuple[dict, list[int]]:
    """Per item, the parts of Δ tied to the bridge word (want: any of w, jw, jwo): w, the least-squares fit on the J++
    directions of the org and alt bridge tokens' one-token variants; jw, signed OMP (k = K) over the letter atoms with
    those variants banned, fit on the whole Δ; jwo, the same fit on Δ - w over the atoms projected off the word's span
    (so it holds none of the word's energy; checked per item). Returns ({part: [n, d]}, variants per item)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts.exp04_brew_parts import signed_omp

    row_of = {int(t): i for i, t in enumerate(letters.tolist())}
    out = {d: torch.zeros_like(x) for d in want | {"w"}}
    n_var = []
    for i, c in enumerate(progress(cases if want else [], "word and J++-without-word parts (case)")):
        ban = variant_ids(tok, [c["bridge"], c["cf_bridge"]])
        n_var.append(len(ban))
        v = lens.vectors(layer, torch.tensor(ban, device="cuda"))  # [m, d] unit
        out["w"][i] = torch.linalg.lstsq(v.T, x[i][:, None]).solution[:, 0] @ v
        keep = torch.ones(len(letters), dtype=torch.bool, device="cuda")
        keep[[row_of[b] for b in ban if b in row_of]] = False
        if "jw" in want:
            out["jw"][i] = signed_omp(jdic[keep], x[i : i + 1], K)[0]
        if "jwo" in want:
            q = torch.linalg.qr(v.T.float()).Q  # [d, m]
            dk = jdic[keep].float()
            dk.addmm_(dk @ q, q.T, alpha=-1.0)
            norm = dk.norm(dim=-1, keepdim=True)
            dk.mul_((norm > 1e-3) / norm.clamp_min(1e-3))  # atoms (almost) inside the word's span: zero rows
            out["jwo"][i] = signed_omp(dk, (x[i] - out["w"][i])[None], K)[0]
            del dk
            leak = float((out["jwo"][i] @ q).norm() ** 2 / out["jwo"][i].norm().clamp_min(1e-30) ** 2)
            assert leak < 1e-3, f"jwo holds {leak:.2e} of its energy in the word's span ({c['scene']})"
    return out, n_var


def keep_cells(rows: list[dict], n_boot: int) -> list[dict]:
    """The keep-only arms (arm keep_part / keep_rand per dict): per dict and reader, the part alone's switches as a
    share of the whole change's, the random part alone's, and their paired difference (cluster bootstrap)."""
    from scripts import x0_amnesic as AM

    out = []
    for d in sorted({r["dict"] for r in rows if r["arm"] == "keep_part"}):
        for w in X.READERS:
            mine = [r for r in rows if r["reader"] == w and (r["arm"] == "whole" or r["dict"] == d)]
            scenes = sorted({r["scene"] for r in mine})
            got = {(r["scene"], r["arm"]): r["switched"] for r in mine}
            ent = {r["scene"]: r["entity"] for r in mine}
            sw = {a: [got[(s, a)] for s in scenes] for a in ("whole", "keep_part", "keep_rand")}
            r_ = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
            s = {a: float(np.mean(v)) for a, v in sw.items()}
            out.append({"part": d, "reader": w, "n": len(scenes), "S": s,
                        "kept": AM.with_ci(AM.of_whole, s, r_, "keep_part"),
                        "rand_kept": AM.with_ci(AM.of_whole, s, r_, "keep_rand"),
                        "difference": AM.paired(AM.of_whole, s, r_, "keep_part", "keep_rand")})  # fmt: skip
    return out


def stage_run(
    name: str, single: str, x0b: str | None = None, used: tuple[str, ...] | None = None, keep: tuple[str, ...] = ()
) -> Path:
    """The single-change run's items (the four parts, or `used`), or with x0b an X0b run's eligible items (w, jw, jpp:
    Dan's item 6, the X0b arms). keep: parts also pasted alone, against the random part of their share alone (Dan,
    25 Oct ~00:20)."""
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    from scripts import x0b_generalize as B

    src_dir = B.RESULTS / x0b if x0b else X.RESULTS / single
    sm = json.loads((src_dir / "manifest.json").read_text())
    assert x0b or sm["alt"] == "single", f"{single} is not a single-change run"
    used = used or (("w", "jw", "jpp") if x0b else PARTS)
    assert "pca_eq" not in used or "jpp" in used, "pca_eq matches the jpp part's share: run jpp beside it"
    assert set(keep) <= set(used), "a kept part must be one of the parts"
    layer = sm["predicted"]
    scenes = sorted({r["scene"] for r in X.read_jsonl(src_dir / "outcomes.jsonl") if r["rendering"] == "chat"})
    X.ALT = "single"
    model = load_model()
    lens = JLens(model, "jpp")
    tok = model.tokenizer
    cases, _ = B.build_cases(tok, sm["set"]) if x0b else X.build_cases(tok, sm["set"])
    by_scene = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    cases = [by_scene[s] for s in scenes]
    pca, pca_info = pca_dictionary(model, layer) if {"pca", "pca_eq"} & set(used) else (None, None)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "single": x0b or single, "source_exp": "x0b_generalize" if x0b else X.EXP, "single_code": sm["code"],
         "set": sm["set"], "layer": layer, "items": len(scenes), "k": K, "parts": list(used), "keep": list(keep), "pca": pca_info, "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(),
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED, "held_out": HELD_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(json.dumps(pca_info), flush=True)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    letters = model.letter_token_ids()
    jdic = lens.vectors(layer, letters)
    with torch.no_grad():
        h_org, deltas = [], []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {
                v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                for v in ("org", "alt")
            }  # .to: a model split over two GPUs (the 122B) records this layer on either
            h_org.append(h["org"].float())
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        parts = {"jpp": X.fit(jdic, x, K, "signed")}
        if pca is not None:
            parts["pca"] = X.fit(pca, x, K, "signed")
        if "pca_eq" in used:
            jshare = parts["jpp"].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            parts["pca_eq"], k_eq = equal_share(pca, x, jshare)
            coef = x @ pca.T  # the check: the top-K |coefficient| part is signed OMP's k = K part on these atoms
            idx = coef.abs().topk(K, dim=-1).indices
            mine = torch.zeros_like(coef).scatter(-1, idx, coef.gather(-1, idx)) @ pca
            err = float(((mine - parts["pca"]).norm(dim=-1) / parts["pca"].norm(dim=-1).clamp_min(1e-30)).max())
            assert err < 1e-3, f"top-|coef| order differs from signed OMP on the PCA atoms (max rel. err {err:.2e})"
        words, n_var = word_parts(lens, tok, layer, letters, jdic, cases, x, {"w", "jw", "jwo"} & set(used))
        parts.update(words)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        arms, shares = {X.WHOLE: x}, []
        for d in used:
            share = parts[d].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            rand = SP.random_subspace_part(x, share, basis)
            fit = {"w": "lsq", "pca_eq": "eq"}.get(d, "signed")
            k = 0 if d in ("w", "pca_eq") else K
            arms[(d, k, fit, "no_part")] = x - parts[d]
            arms[(d, k, fit, "no_rand")] = x - rand
            if d in keep:
                arms[(d, k, fit, "keep_part")], arms[(d, k, fit, "keep_rand")] = parts[d], rand
            shares += [{"scene": c["scene"], "dict": d, "k": k, "omp": fit, "share": round(float(share[i]), 5),
                        **({"variants": n_var[i]} if d == "w" else {}),
                        **({"k_eq": int(k_eq[i])} if d == "pca_eq" else {})} for i, c in enumerate(cases)]  # fmt: skip
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
    k_eq = [s["k_eq"] for s in shares if s["dict"] == "pca_eq"]
    label = {"w": "word only (least squares)", "jw": "J++ without the word (k = 25)", "pca": f"PCA top {N_PCA} (k = 25)",
             "jpp": "J++ (k = 25, reference)", "pca_eq": f"PCA top {N_PCA} at J++'s share (k per item)",
             "jwo": "J++ without the word, orthogonal to the word (k = 25)"}  # fmt: skip
    lines = [f"# Word, J++ without the word, PCA: {name}", "",
             f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, the single-change items of {m['single']} (n = "
             f"{m['items']}); each part removed against a random subspace of its own share; bootstrap over bridge entities "
             f"({n_boot} resamples). "
             + (f"Word variants per item: median {statistics.median(nvar)} (range {min(nvar)}-{max(nvar)}). " if nvar else "")
             + (f"PCA at J++'s share (Dan, ~21:50): atoms per item median {statistics.median(k_eq)} (range {min(k_eq)}-"
                f"{max(k_eq)}). " if k_eq else "")
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
    if k_eq:
        lk, rc = (next(b for b in blob if b["part"] == "pca_eq" and b["reader"] == w)["excess"] for w in X.READERS)
        branch = ("recall-specific like J++" if lk[0] <= 0.10 and rc[0] >= 0.20 and rc[1] > 0 else
                  "hurts both readers" if lk[0] >= 0.10 and lk[1] > 0 and rc[1] > 0 else
                  "inert" if lk[2] < 0.10 and rc[2] < 0.10 else "none of the three branches")  # fmt: skip
        lines += ["", "Reading for PCA at J++'s share (Dan, ~21:50, before the run): recall-specific like J++ -> 'J++-specific' "
                  "means 'aligned with the layer's main directions'; hurts both readers -> J++ is the only dictionary that "
                  "separates the readers; inert -> J++ is special at equal share. Branches (Q30.1, committed before the "
                  "run): recall-specific = lookup excess <= 0.10, recall excess >= 0.20 with lower CI > 0; hurts both = "
                  "lookup excess >= 0.10 and both readers' lower CI > 0; inert = both readers' upper CI < 0.10. This run: "
                  f"lookup {X.fmt3(lk)}, recall {X.fmt3(rc)} -> {branch}."]  # fmt: skip
    if "jwo" in used:
        rc = next(b for b in blob if b["part"] == "jwo" and b["reader"] == X.RECALL)["excess"]
        branch = ("recall needs J++ components beyond the word" if rc[0] >= 0.20 else "the word and the other J++ "
                  "components are redundant: either suffices" if rc[0] <= 0.10 else "neither branch (between 0.10 and 0.20)")  # fmt: skip
        lines += ["", "Reading for the word-orthogonal part (Dan, ~22:05; no prediction committed before the run): recall "
                  "still loses >= 0.20 with the word intact -> 'recall needs J++ components beyond the word'; <= 0.10 -> "
                  "'the word and the other J++ components are redundant: either suffices'. 'Loses' (set by the agent "
                  f"before the run): the point estimate of the recall's excess. This run: {X.fmt3(rc)} -> {branch}."]  # fmt: skip
    kept = keep_cells(rows, n_boot) if m.get("keep") else []
    if kept:
        lines += ["", "## Each part pasted alone (Dan, 25 Oct ~00:20): its switches as a share of the whole change's, against "
                  "the random part of its share alone", "", "| part | reader | n | kept / whole | random kept / whole | "
                  "difference |", "|---|---|---|---|---|---|"]  # fmt: skip
        lines += [f"| {label[k['part']]} | {'lookup' if k['reader'] == X.LOOKUP else 'recall'} | {k['n']} | {X.fmt3(k['kept'])} | "
                  f"{X.fmt3(k['rand_kept'])} | {X.fmt3(k['difference'])} |" for k in kept]  # fmt: skip
    (out / "verdict.json").write_text(
        json.dumps({"run": name, "manifest": m, "rows": blob, "kept": kept}, indent=1) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--single", default="x0_single_27b_r2")
    ap.add_argument("--x0b", default=None, help="run: an X0b run's eligible items instead (parts w, jw, jpp)")
    ap.add_argument("--parts", default=None, help=f"run: comma-separated, of {PARTS}, pca_eq, jwo (default: {PARTS})")
    ap.add_argument("--keep", default="", help="run: comma-separated parts also pasted alone (keep-only arms)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        used = tuple(a.parts.split(",")) if a.parts else None
        assert used is None or set(used) <= {*PARTS, "pca_eq", "jwo"}, used
        stage_run(a.name, a.single, a.x0b, used, tuple(k for k in a.keep.split(",") if k))
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
