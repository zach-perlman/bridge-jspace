"""paper_swap_decomp (Zach, 2026-10-30, prereg amendment 65 note 39): the J-space paper's intermediate swap on its own 90
two-hop prompts (data/probe_swap.json), decomposed into the answer category's J-directions and the rest.

Items and gate (exp02_swaps' `prepare`, no probes, as exp14): the prompt with its trailing space stripped; eligible if
the clean greedy continuation has the answer and not the swap answer (exp13's criterion C), and the intermediate, swap
target, answer and swap answer each have a single-token surface (first-token scoring and the concept-token atoms need
them). Chat prefill (exp02's chat_prefill) only if fewer than 50 of the 90 are raw-eligible (--prompt-end auto, full runs).
Sets (data/paper_answer_types.json, frozen before any run): primary (closed answer vocabulary), side_table (answer type =
the intermediate's, or the own answer's token is a name token for this tokenizer), own_pair_only (no closed vocabulary).

Swap: clamp.SwapClamp at every layer of a window, every position from 1, as exp02's raw_jlens: the clean coordinates on
two unit lens vectors (the concept tokens) exchanged. The arms differ only in the two atoms:
  1 bridge         intermediate <-> swap_to (the paper's swap; exp02's raw_jlens)
  2 answer         answer <-> swap_answer (exp14's "answer")
  3 bridge_noA     arm 1's atoms orthogonalised to an orthonormal basis of span(A), renormalised (note 13's clamp_noans
                   route); A = the item's scrub set (its answer type's vocabulary, all first-token forms, own pair
                   included, name tokens excluded)
  4 bridge_noA_nm  arm 3's edit rescaled per position (and layer) to arm 1's edit norm on the same residual
  5 bridge_onlyA   arm 1's atoms projected onto span(A), renormalised
  6 bridge_offA    arm 3 with the item's count-matched off-category set (the vocabulary file's "off")
  7 bridge_randA   arm 3 with as many random letter tokens (seeded per item; never a scrub or name token)
  8 bridge_ownA    arm 3 with the own answer pair's forms only
  9 null           exp02's matched-norm null for arms 1, 2 and 5: each position's edit replaced by a random unit
                   direction (one per layer, seeded exp02-style: NULL_SEED + 1000 * item index + arm index; arm 1 is
                   exp02's raw_jlens seed, arm 2 exp14's answer seed) scaled to that edit's norm
Own-pair-only items run arms 1, 2, 8 and the nulls of 1 and 2. A layer whose two atoms are near-parallel (exp02) or
whose orthogonalised / projected atom has norm < 1e-6 is skipped and counted.
Windows: cumulative from the workspace start (27B L16 -> 20, 24, ..., 60; 9B L6 -> 8, ..., 30; Lightning L8 -> 12, ...,
48; Muse, not in note 39: Lightning's, same depth), plus the main band (27B L24-40, exp02's; the others: note 20's band
extended earlier by 1/8 of the depth, as L24-40 extends the 27B's note-20 band L32-40: 9B L8-16, Lightning L20-33, Muse
L29-42). Each window's arms run as one batch with a clean row (same-batch numerics for delta log p).
Read: "flip" = the swap answer's first token (any single-token surface) at word rank 1 of the next-token logits
(formatting tokens excluded, strict: exp02's rank scoring), delta log p of the swap answer and the answer beside; flip_eq
also accepts the number twin (4 <-> four, exp13's forms; descriptive). Greedy check (exp02's `swap`, criterion C) at the
main band for arms 1, 2, 3, 5 and the nulls of 1, 2, 5. Per row: |edit|/|h| (last position; mean over positions), the
edit's squared share in span(A) (shareA; arm 1's is note 39's diagnostic), layers edited / skipped.
Lenses: the model's frozen J++ (published for the 27B and 9B; ours for Lightning and Muse); on the 27B also the plain J-lens.
27B with --repro-gate: before the windows, arm 1 at L24-40 (J++) is checked against exp02 main_v4_jpp's raw_jlens
outcomes on the shared items (greedy flip rate inside exp02's Wilson 95% interval on those items); the run stops if not.

python scripts/paper_swap_decomp.py --name N --why W [--limit K | --items A B ...] [--n-windows K] [--repro-gate]
       [--prompt-end auto|stripped|chat_prefill]
python scripts/paper_swap_decomp.py --check      (CPU: vocabulary, tokenizer, lens layers, arm mechanics, plan)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from bridge_jspace.clamp import SwapClamp, near_parallel  # noqa: E402

EXP = "paper_swap_decomp"
RES = pins.RESULTS_DIR / EXP
VOCAB = pins.DATA_DIR / "paper_answer_types.json"
VOCAB_SHA256 = "a93fc6342cf6fa1d59a5af9370e324bf40cc6cce5b030fe95312935f24b2abf0"
EXP02_REF = pins.RESULTS_DIR / "exp02_swaps" / "main_v4_jpp"  # the 27B's A0 anchor: raw_jlens 49% [38, 60], null 0%

# (start, window ends): the paper's cumulative windows from the workspace start (note 39)
WINDOWS = {
    "qwen3.6-27b": (16, list(range(20, 61, 4))),
    "qwen3.5-9b": (6, list(range(8, 31, 2))),
    "nemotron-3.5-lightning": (8, list(range(12, 49, 4))),
    "muse-glimmer-30b": (8, list(range(12, 49, 4))),  # not in note 39 (descriptive): Lightning's, same 52 blocks
}
MAIN_BAND = {"qwen3.6-27b": (24, 40), "qwen3.5-9b": (8, 16), "nemotron-3.5-lightning": (20, 33), "muse-glimmer-30b": (29, 42)}
NOTE20_BAND = {"qwen3.6-27b": (32, 40), "qwen3.5-9b": (12, 16), "nemotron-3.5-lightning": (27, 33), "muse-glimmer-30b": (36, 42)}
LENSES = {"qwen3.6-27b": ("jpp", "jlens")}  # others: their frozen J++ only
ARMS = ("bridge", "answer", "bridge_noA", "bridge_noA_nm", "bridge_onlyA", "bridge_offA", "bridge_randA", "bridge_ownA")
OWN_PAIR_ARMS = ("bridge", "answer", "bridge_ownA")
NULL_ARMS = ("bridge", "answer", "bridge_onlyA")
GREEDY_ARMS = ("bridge", "answer", "bridge_noA", "bridge_onlyA")
SCRUB_OF = {"bridge_noA": "scrub", "bridge_noA_nm": "scrub", "bridge_onlyA": "scrub", "bridge_offA": "off",
            "bridge_randA": "rand", "bridge_ownA": "own"}  # fmt: skip
NULL_SEED = 0  # exp02's
MIN_ATOM_NORM = 1e-6
CHAT_FALLBACK_BELOW = 50


def arm_index(arm: str) -> int:
    return ARMS.index(arm)


def windows_for(target: str, n_windows: int | None = None) -> list[tuple[int, int, bool]]:
    """(start, end, is_main) per window: the cumulative windows, then the main band."""
    start, ends = WINDOWS[target]
    ends = ends[:n_windows] if n_windows else ends
    return [(start, e, False) for e in ends] + [(*MAIN_BAND[target], True)]


def wname(start: int, end: int) -> str:
    return f"{start}-{end}"


def load_vocab() -> dict:
    raw = VOCAB.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    assert got == VOCAB_SHA256, f"{VOCAB} sha256 {got} != frozen {VOCAB_SHA256}"
    return json.loads(raw)


def item_set(vocab: dict, name: str, target: str) -> str:
    """primary / side_table / own_pair_only for this tokenizer (own_answer_token_excluded -> side_table)."""
    row = vocab["items"][name]
    if row["set"] == "primary" and row["tokens"][target]["own_answer_token_excluded"]:
        return "side_table"
    return row["set"]


# ---- arm mechanics (device-agnostic; checked on CPU by --check) ------------------------------------------------


def basis(vecs: torch.Tensor) -> torch.Tensor:
    """An orthonormal basis [d, r] of the rows' span (rank-revealing SVD in double, nn_swap's basis())."""
    U, sv, _ = torch.linalg.svd(vecs.T.double(), full_matrices=False)
    return U[:, sv > sv[0] * 1e-6].float()


def arm_atoms(pair: torch.Tensor, Q: torch.Tensor | None, mode: str) -> tuple[torch.Tensor | None, list[float]]:
    """The two atoms of an arm at one layer: `pair` [2, d] unit; mode "plain", "orth" (off span(Q)) or "proj" (onto it),
    renormalised. Returns (atoms or None if degenerate, each row's pre-renormalisation norm)."""
    if mode == "plain":
        return pair, [1.0, 1.0]
    inside = (pair @ Q) @ Q.T
    rows = pair - inside if mode == "orth" else inside
    norms = rows.norm(dim=-1)
    if float(norms.min()) < MIN_ATOM_NORM:
        return None, norms.tolist()
    return rows / norms[:, None], norms.tolist()


def _record(edit, h: torch.Tensor, delta: torch.Tensor, Q: torch.Tensor | None) -> torch.Tensor:
    edit.edit_ratio_last = float(delta[-1].norm() / h[-1].norm())
    edit.edit_ratio_edited = float((delta.norm(dim=-1) / h[1:].norm(dim=-1))[edit.mask].mean())
    tot = float(delta.pow(2).sum())
    edit.share = float((delta @ Q).pow(2).sum()) / tot if Q is not None and tot > 0 else math.nan
    out = h.clone()
    out[1:] += delta
    return out


class Clamp(SwapClamp):
    """exp02's SwapClamp, also recording the edit's squared share in span(Q) (shareA) per call."""

    def __init__(self, atoms, clean_h, null_direction=None, share_basis=None):
        super().__init__(atoms, clean_h, null_direction=null_direction)
        self.share_basis, self.share = share_basis, math.nan

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        return _record(self, h, self.delta(h), self.share_basis)


class NormMatched:
    """Arm 4: arm 3's edit rescaled, per position, to arm 1's edit norm on the same residual."""

    def __init__(self, c1: SwapClamp, c3: SwapClamp, share_basis=None):
        self.c1, self.c3, self.mask, self.share_basis = c1, c3, c3.mask, share_basis
        self.edit_ratio_last = self.edit_ratio_edited = self.share = math.nan

    def delta(self, h: torch.Tensor) -> torch.Tensor:
        d1, d3 = self.c1.delta(h), self.c3.delta(h)
        n1, n3 = d1.norm(dim=-1, keepdim=True), d3.norm(dim=-1, keepdim=True)
        return torch.where(n3 > 0, d3 * n1 / n3.clamp_min(1e-30), torch.zeros_like(d3))

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        return _record(self, h, self.delta(h), self.share_basis)


def null_directions(seed: int, layers: list[int], d: int, device) -> dict[int, torch.Tensor]:
    """exp02's null: one random unit direction per layer, drawn in layer order from one generator (skips do not shift)."""
    g = torch.Generator(device=device).manual_seed(seed)
    return {la: torch.nn.functional.normalize(torch.randn(d, device=device, generator=g), dim=0) for la in layers}


def build_edits(arm: str, layers: list[int], atoms: dict, clean_h: dict, Qs: dict, null_seed: int | None) -> tuple[dict, list[int]]:
    """Per-layer edits of one arm over a window. atoms[(arm_key, layer)] -> (atoms | None); Qs[layer]['scrub'] = span(A)
    (the share basis). Returns ({layer: edit}, skipped layers)."""
    dirs = null_directions(null_seed, layers, next(iter(clean_h.values())).shape[1], next(iter(clean_h.values())).device) if null_seed is not None else {}
    edits, skipped = {}, []
    for la in layers:
        QA = Qs[la].get("scrub") if Qs else None
        if arm == "bridge_noA_nm":
            a1, a3 = atoms[("bridge", la)], atoms[("bridge_noA", la)]
            if a1 is None or a3 is None or near_parallel(a1[0], a1[1]) or near_parallel(a3[0], a3[1]):
                skipped.append(la)
                continue
            edits[la] = NormMatched(SwapClamp(a1, clean_h[la]), SwapClamp(a3, clean_h[la]), share_basis=QA)
            continue
        a = atoms[(arm, la)]
        if a is None or near_parallel(a[0], a[1]):
            skipped.append(la)
            continue
        edits[la] = Clamp(a, clean_h[la], null_direction=dirs.get(la), share_basis=QA)
    return edits, skipped


def edit_stats(edits: dict) -> dict:
    vals = list(edits.values())
    mean = lambda xs: statistics.mean(xs) if xs else math.nan  # noqa: E731
    shares = [e.share for e in vals if not math.isnan(e.share)]
    return {"edit_ratio_last": mean([e.edit_ratio_last for e in vals]), "edit_ratio_edited": mean([e.edit_ratio_edited for e in vals]),
            "shareA": mean(shares), "layers_edited": len(vals)}  # fmt: skip


# ---- model-side helpers ----------------------------------------------------------------------------------------


class NoProbes:
    """exp02's `prepare` drops questions whose entities have no exp01 probe; lens-vector swaps need none (exp14's)."""

    class _Everything:
        def __contains__(self, _: object) -> bool:
            return True

    index = _Everything()


def batched_logits(model, ids: torch.Tensor, row_edits: list[dict]) -> torch.Tensor:
    """Final-position logits [B, vocab] (fp32) of one batched forward of one prompt, row r with edits row_edits[r]
    (a row without an edit at a layer passes through)."""
    from bridge_jspace.model import _forward_hooks

    batch = ids.expand(len(row_edits), -1).contiguous()

    def hook_for(la):
        def hook(_m, _a, out):
            h = out[0] if isinstance(out, tuple) else out
            h = h.clone()
            for r, e in enumerate(row_edits):
                if la in e:
                    h[r] = e[la](h[r].float()).to(h.dtype)
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    layers = sorted({la for e in row_edits for la in e})
    with _forward_hooks([(model.layers[la], hook_for(la)) for la in layers]):
        out = model.hf(input_ids=batch, attention_mask=torch.ones_like(batch), use_cache=False, logits_to_keep=1)
    return out.logits[:, -1].float()


def number_twin_ids(model, word: str) -> list[int]:
    """Single-token surfaces of the answer's other number form (exp13's answer_forms: '4' <-> 'four')."""
    from scripts.exp13_greedy_answers.experiment import answer_forms

    out: set[int] = set()
    for form in answer_forms(word)[1:]:
        if len(form) == 1:
            out |= set(model.surface_ids(form[0]))
    return sorted(out)


def read_row(model, logits: torch.Tensor, clean_logits: torch.Tensor, ids_: dict) -> dict:
    lp, lp0 = torch.log_softmax(logits, -1), torch.log_softmax(clean_logits, -1)
    lse = lambda x, s: float(torch.logsumexp(x[s], 0))  # noqa: E731
    swap_rank, clean_rank = model.word_rank(logits, ids_["swap"]), model.word_rank(logits, ids_["answer"])
    return {
        "flip": swap_rank == 1, "kept": clean_rank == 1,
        "flip_eq": model.word_rank(logits, sorted(set(ids_["swap"]) | set(ids_["swap_eq"]))) == 1,
        "swap_rank": swap_rank, "clean_rank": clean_rank, "top_word": model.top_word(logits), "top1_raw": int(logits.argmax()),
        "logp_swap": lse(lp, ids_["swap"]), "logp_answer": lse(lp, ids_["answer"]),
        "dlogp_swap": lse(lp, ids_["swap"]) - lse(lp0, ids_["swap"]), "dlogp_answer": lse(lp, ids_["answer"]) - lse(lp0, ids_["answer"]),
    }  # fmt: skip


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def repro_check(greedy_rows: list[dict], first_rows: list[dict]) -> dict:
    """A0 reproduction (27B): our arm 1 at L24-40 (J++) vs exp02 main_v4_jpp's raw_jlens on the shared items."""
    from bridge_jspace.stats import wilson

    ref = [json.loads(x) for x in (EXP02_REF / "outcomes.jsonl").read_text().splitlines() if x.strip()]
    theirs = {(o["name"], o["null"]): o for o in ref if o["condition"] == "raw_jlens" and o["band"] == "24-40"}
    ours = {(o["name"], o["null"]): o for o in greedy_rows if o["arm"] == "bridge" and o["lens"] == "jpp" and o["band"] == "24-40"}
    out: dict = {"exp02_run": str(EXP02_REF.relative_to(pins.REPO_ROOT)), "exp02_cell_all": "49% [38, 60] (n 77), null 0%"}
    for null in (False, True):
        shared = sorted(n for (n, nl) in set(ours) & set(theirs) if nl == null)
        a = [bool(ours[(n, null)]["flip"]) for n in shared]
        b = [bool(theirs[(n, null)]["flip"]) for n in shared]
        fa = [ours[(n, null)]["swap_rank"] == 1 for n in shared]
        fb = [theirs[(n, null)]["swap_rank"] == 1 for n in shared]
        w_ours, w_theirs = wilson(sum(a), len(a)), wilson(sum(b), len(b))
        out["null" if null else "real"] = {
            "n_shared": len(shared), "greedy_flip_ours": w_ours, "greedy_flip_exp02": w_theirs,
            "agree": sum(x == y for x, y in zip(a, b)), "ours_only": sum(x and not y for x, y in zip(a, b)),
            "exp02_only": sum(y and not x for x, y in zip(a, b)),
            "first_token_flip_ours": sum(fa) / len(fa) if fa else None, "first_token_flip_exp02": sum(fb) / len(fb) if fb else None,
        }  # fmt: skip
    real = out["real"]
    lo, hi = real["greedy_flip_exp02"][1], real["greedy_flip_exp02"][2]
    out["reproduced"] = bool(real["n_shared"]) and lo <= real["greedy_flip_ours"][0] <= hi
    out["rule"] = "reproduced if our greedy flip rate on the shared items lies inside exp02's Wilson 95% interval on them"
    out["n_eligible_ours"], out["only_ours"] = len({n for (n, nl) in ours if not nl}), sorted({n for (n, nl) in ours if not nl} - {n for (n, nl) in theirs})
    out["only_exp02"] = sorted({n for (n, nl) in theirs if not nl} - {n for (n, nl) in ours})
    # the windows loop's batched first-token read of arm 1 at L24-40 vs exp02's first-token rank (both strict word rank 1)
    first = {(o["name"], o["null"]): o["flip"] for o in first_rows
             if o["arm"] == "bridge" and o["lens"] == "jpp" and o["window"] == "24-40"}  # fmt: skip
    for null in (False, True):
        shared = sorted(n for (n, nl) in set(first) & set(theirs) if nl == null)
        if shared:
            out["null" if null else "real"]["batched_first_token"] = {
                "n": len(shared), "ours": sum(first[(n, null)] for n in shared) / len(shared),
                "exp02": sum(theirs[(n, null)]["swap_rank"] == 1 for n in shared) / len(shared),
                "agree": sum(first[(n, null)] == (theirs[(n, null)]["swap_rank"] == 1) for n in shared)}
    return out


# ---- the run ---------------------------------------------------------------------------------------------------


@torch.no_grad()
def run(a) -> None:
    from bridge_jspace.data import load_items
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts.exp02_swaps import prepare
    from scripts.exp02_swaps import swap as exp02_swap

    target = pins.TARGET
    pins.check_run_name(a.name)
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    vocab = load_vocab()
    items_all = load_items()
    picked = [(i, it) for i, it in enumerate(items_all) if (not a.items or it["name"] in a.items)][: a.limit or None]
    full = len(picked) == len(items_all)
    wins = windows_for(target, a.n_windows)
    lenses = LENSES.get(target, ("jpp",))
    layers_all = sorted({la for s, e, _ in wins for la in range(s, e + 1)})
    manifest = {
        "exp": EXP, "run": a.name, "why": a.why, "note": "prereg amendment 65, note 39", "target": target,
        "model": pins.model_pin(), "lenses": {ln: list(pins.LENS_SOURCES[ln]) for ln in lenses},
        "items": {"file": "data/probe_swap.json", "sha256": pins.PROBE_SWAP_SHA256, "n_run": len(picked), "full": full},
        "vocabulary": {"file": "data/paper_answer_types.json", "sha256": VOCAB_SHA256},
        "windows": [wname(s, e) for s, e, m in wins if not m], "main_band": wname(*MAIN_BAND[target]),
        "main_band_rule": f"note 20's band {wname(*NOTE20_BAND[target])} extended earlier by 1/8 of the depth (as exp02's 27B L24-40 extends L32-40)",
        "arms": list(ARMS), "null_arms": list(NULL_ARMS), "greedy_arms": list(GREEDY_ARMS), "own_pair_arms": list(OWN_PAIR_ARMS),
        "seeds": {"null": "NULL_SEED 0 + 1000 * item index + arm index (exp02 raw_jlens = bridge 0, exp14 answer 1)",
                  "rand_atoms": "random.Random('n39rand:<target>:<item>')", "off": "frozen in the vocabulary file"},
        "prompt_end": a.prompt_end, "chat_fallback_below": CHAT_FALLBACK_BELOW, "repro_gate": a.repro_gate,
        "positions": "every position from 1 (exp02's 'all')",
        "flip": "swap answer's single-token surfaces at word rank 1 of the next-token logits (strict, formatting excluded)",
        "command": " ".join(sys.argv), "git_state": pins.git_state(), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    model = load_model()
    lens_objs = {ln: JLens(model, ln) for ln in lenses}
    n_vocab = model.hf.lm_head.weight.shape[0]
    letters = model.letter_token_ids().tolist()
    print(f"[{a.name}] model and lenses loaded {time.time() - t0:.0f}s; windows {[wname(s, e) for s, e, _ in wins]}", flush=True)

    # phase 0: the gate (and the chat fallback), then arm 1's greedy check at the main band
    def gate(prompt_end: str):
        rows, prep = [], {}
        for index, item in picked:
            row, prepared = prepare(model, NoProbes(), item, layers_all, "greedy_c", prompt_end)
            row.update(index=index, prompt_end=prompt_end, set=item_set(vocab, item["name"], target),
                       answer_type=vocab["items"][item["name"]]["answer_type"])  # fmt: skip
            multi = [f for f in ("intermediate", "swap_to", "answer", "swap_answer") if not model.surface_ids(item[f])]
            if row["status"] == "eligible" and multi:
                row["status"] = "multi_token:" + "+".join(multi)
            if row["status"] == "eligible":
                ids, clean_h, answer_ids, swap_ids = prepared
                prep[item["name"]] = (ids, {la: clean_h[la].cpu() for la in layers_all}, answer_ids, swap_ids)
            rows.append(row)
        return rows, prep

    prompt_end = "stripped" if a.prompt_end == "auto" else a.prompt_end
    item_rows, prep = gate(prompt_end)
    n_raw = sum(r["status"] == "eligible" for r in item_rows)
    decision = {"raw_eligible": n_raw if prompt_end == "stripped" else None, "prompt_end": prompt_end}
    if a.prompt_end == "auto" and full and n_raw < CHAT_FALLBACK_BELOW:
        print(f"[{a.name}] raw-eligible {n_raw} < {CHAT_FALLBACK_BELOW}: chat_prefill fallback", flush=True)
        prompt_end = "chat_prefill"
        item_rows, prep = gate(prompt_end)
        decision.update(prompt_end=prompt_end, chat_eligible=sum(r["status"] == "eligible" for r in item_rows))
    print(f"[{a.name}] gate: {decision}; statuses {dict(statistics_counter(r['status'] for r in item_rows))} {time.time() - t0:.0f}s", flush=True)

    by_name = {it["name"]: (i, it) for i, it in picked}
    greedy_rows: list[dict] = []
    main_s, main_e = MAIN_BAND[target]
    main_layers = list(range(main_s, main_e + 1))

    def pair_tokens(item, kind):
        f = ("intermediate", "swap_to") if kind == "bridge" else ("answer", "swap_answer")
        return [model.concept_token(item[f[0]]), model.concept_token(item[f[1]])]

    def greedy(item, index, lens_name, arm, atoms_by_layer, null):
        ids, clean_cpu, answer_ids, swap_ids = prep[item["name"]]
        clean_h = {la: clean_cpu[la].cuda() for la in main_layers}
        seed = NULL_SEED + 1000 * index + arm_index(arm) if null else None
        r = exp02_swap(model, ids, clean_h, atoms_by_layer, item, answer_ids, swap_ids, seed, "greedy_c")
        greedy_rows.append({"name": item["name"], "lens": lens_name, "band": wname(main_s, main_e), "arm": arm, "null": null, **r})

    primary_lens = lenses[0]
    for name in prep:
        index, item = by_name[name]
        b = torch.tensor(pair_tokens(item, "bridge"), device="cuda")
        atoms = {la: lens_objs[primary_lens].vectors(la, b) for la in main_layers}
        for null in (False, True):
            greedy(item, index, primary_lens, "bridge", atoms, null)
    print(f"[{a.name}] phase 0: arm 1 greedy at {wname(main_s, main_e)} on {len(prep)} items {time.time() - t0:.0f}s", flush=True)
    repro = None
    if target == "qwen3.6-27b":
        repro = repro_check(greedy_rows, [])
        (out_dir / "repro.json").write_text(json.dumps(repro, indent=2) + "\n")
        print(f"[{a.name}] A0 reproduction vs exp02 main_v4_jpp: {json.dumps(repro['real'])} reproduced={repro['reproduced']}", flush=True)
        if a.repro_gate and not repro["reproduced"]:
            write_jsonl(out_dir / "items.jsonl", item_rows)
            write_jsonl(out_dir / "greedy.jsonl", greedy_rows)
            raise SystemExit(f"[{a.name}] A0 reproduction FAILED (see repro.json); stopping before the windows")

    # phase 1: the windows
    rows: list[dict] = []
    atom_rows: list[dict] = []
    for name in prep:
        index, item = by_name[name]
        ids, clean_cpu, answer_ids, swap_ids = prep[name]
        clean_h = {la: clean_cpu[la].cuda() for la in layers_all}
        iset = item_set(vocab, name, target)
        own_only = iset == "own_pair_only"
        arms = OWN_PAIR_ARMS if own_only else ARMS
        nulls = [x for x in NULL_ARMS if x in arms]
        toks = vocab["items"][name]["tokens"][target]
        sets = {"own": toks["own"]}
        assert toks["own"], f"{name}: no own-pair token left after the name exclusion"
        if not own_only:
            sets["scrub"], sets["off"] = toks["scrub"], toks["off"]
            barred = set(toks["scrub"]) | set(toks["excluded"])
            pool = sorted(t for t in letters if t not in barred)
            sets["rand"] = sorted(random.Random(f"n39rand:{target}:{name}").sample(pool, len(toks["scrub"])))
        assert all(max(v) < n_vocab for v in sets.values() if v), "vocabulary ids beyond the lm_head"
        ids_ = {"answer": answer_ids, "swap": swap_ids, "swap_eq": number_twin_ids(model, item["swap_answer"])}
        for lens_name, lens in lens_objs.items():
            bt = torch.tensor(pair_tokens(item, "bridge"), device="cuda")
            at = torch.tensor(pair_tokens(item, "answer"), device="cuda")
            atoms: dict = {}
            Qs: dict = {}
            for la in layers_all:
                B, Aa = lens.vectors(la, bt), lens.vectors(la, at)
                Qs[la] = {k: basis(lens.vectors(la, torch.tensor(v, device="cuda"))) for k, v in sets.items()}
                atoms[("bridge", la)], atoms[("answer", la)] = B, Aa
                share_key = "own" if own_only else "scrub"
                Qs[la]["scrub"] = Qs[la][share_key]  # the share basis: span(A) (own pair for own-pair-only items)
                arow = {"name": name, "lens": lens_name, "layer": la, "set": iset,
                        "diff_cosine": float(torch.nn.functional.cosine_similarity(B[0] - B[1], Aa[0] - Aa[1], dim=0)),
                        "bridge_cos": float(B[0] @ B[1]), "answer_cos": float(Aa[0] @ Aa[1])}  # fmt: skip
                for arm in arms:
                    if arm in SCRUB_OF and arm != "bridge_noA_nm":
                        mode = "proj" if arm == "bridge_onlyA" else "orth"
                        atoms[(arm, la)], norms = arm_atoms(B, Qs[la][SCRUB_OF[arm]], mode)
                        arow[f"{arm}_atom_norms"] = norms
                for k in sets:
                    arow[f"n_{k}"], arow[f"rank_{k}"] = len(sets[k]), int(Qs[la][k].shape[1])
                QA = Qs[la]["scrub"]
                arow["bridge_in_A"] = (B @ QA).pow(2).sum(-1).tolist()  # squared share of each unit bridge atom in span(A)
                arow["answer_in_A"] = (Aa @ QA).pow(2).sum(-1).tolist()
                atom_rows.append(arow)
            for s, e, is_main in wins:
                wl = list(range(s, e + 1))
                plan = [(arm, False) for arm in arms] + [(arm, True) for arm in nulls]
                row_edits, meta = [{}], []
                for arm, null in plan:
                    seed = NULL_SEED + 1000 * index + arm_index(arm) if null else None
                    edits, skipped = build_edits(arm, wl, atoms, clean_h, Qs, seed)
                    row_edits.append(edits)
                    meta.append((arm, null, skipped))
                logits = batched_logits(model, ids, row_edits)
                for r, (arm, null, skipped) in enumerate(meta, start=1):
                    rows.append({"name": name, "index": index, "set": iset, "lens": lens_name, "window": wname(s, e), "start": s,
                                 "end": e, "main": is_main, "arm": arm, "null": null, **read_row(model, logits[r], logits[0], ids_),
                                 **edit_stats(row_edits[r]), "layers_skipped": skipped})  # fmt: skip
                if is_main or (s, e) == (wins[0][0], wins[0][1]):
                    rows.append({"name": name, "index": index, "set": iset, "lens": lens_name, "window": wname(s, e), "start": s,
                                 "end": e, "main": is_main, "arm": "clean", "null": False, **read_row(model, logits[0], logits[0], ids_),
                                 "layers_skipped": []})  # fmt: skip
            # greedy check at the main band: arms 1 (phase 0 for the primary lens), 2, 3, 5 and the nulls of 1, 2, 5
            for arm in GREEDY_ARMS:
                if arm not in arms:
                    continue
                by_layer = {}
                for la in main_layers:
                    at_ = atoms[(arm, la)]
                    by_layer[la] = at_ if at_ is not None else atoms[("bridge", la)][[0, 0]]  # degenerate: near-parallel, skipped
                for null in (False, True) if arm in NULL_ARMS else (False,):
                    if arm == "bridge" and lens_name == primary_lens:
                        continue  # phase 0
                    greedy(item, index, lens_name, arm, by_layer, null)
        print(f"[{a.name}] {name} ({iset}): main-band flips "
              + " ".join(f"{o['arm']}{'/null' if o['null'] else ''}={int(o['flip'])}" for o in rows
                         if o["name"] == name and o["main"] and o["lens"] == primary_lens and o["arm"] != "clean")
              + f" {time.time() - t0:.0f}s", flush=True)  # fmt: skip

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "rows.jsonl", rows)
    write_jsonl(out_dir / "greedy.jsonl", greedy_rows)
    write_jsonl(out_dir / "atoms.jsonl", atom_rows)
    if target == "qwen3.6-27b":
        repro = repro_check(greedy_rows, rows)
        (out_dir / "repro.json").write_text(json.dumps(repro, indent=2) + "\n")
    summary = {
        "gate": decision, "statuses": dict(statistics_counter(r["status"] for r in item_rows)),
        "eligible_by_set": dict(statistics_counter(r["set"] for r in item_rows if r["status"] == "eligible")),
        "rows": len(rows), "greedy_rows": len(greedy_rows), "seconds": round(time.time() - t0),
        "repro": repro, "reader": f"python scripts/paper_swap_read.py results/{EXP}/{a.name}",
    }  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def statistics_counter(xs) -> dict:
    out: dict = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


# ---- --check: CPU dry run ----------------------------------------------------------------------------------------


def check() -> None:
    """Vocabulary, tokenizer, lens layers, arm mechanics and the plan, with no GPU and no model weights."""
    from bridge_jspace.data import load_items
    from bridge_jspace.tokens import load_tokenizer, surface_ids

    target = pins.TARGET
    vocab = load_vocab()
    items = load_items()
    assert set(vocab["items"]) == {it["name"] for it in items}
    tok = load_tokenizer()
    # 1. the vocabulary was built with this tokenizer: its recorded token strings decode the same
    tt = vocab["type_tokens"][target]
    bad = [(ty, i, s) for ty, m in tt.items() for i, s in m.items() if tok.decode([int(i)]) != s]
    assert not bad, f"vocabulary token strings differ under this tokenizer: {bad[:5]}"
    # 2. sets and single-token eligibility (the CPU part of the gate)
    counts: dict = {}
    multi: dict = {}
    for it in items:
        s = item_set(vocab, it["name"], target)
        miss = [f for f in ("intermediate", "swap_to", "answer", "swap_answer") if not surface_ids(tok, it[f])]
        counts.setdefault(s, [0, 0])
        counts[s][0] += 1
        counts[s][1] += not miss
        if miss:
            multi[it["name"]] = miss
    print(f"{target}: per set [items, single-token ok]: {counts}")
    print(f"  no single-token surface: {multi}")
    # 3. lens layers cover every window
    wins = windows_for(target)
    need = sorted({la for s, e, _ in wins for la in range(s, e + 1)})
    for ln in LENSES.get(target, ("jpp",)):
        src = pins.LENS_SOURCES[ln]
        if src[0] == "local":
            path = pins.REPO_ROOT / src[1]
        else:
            from huggingface_hub import hf_hub_download

            path = Path(hf_hub_download(src[0], src[1], revision=src[2], local_files_only=True))
        blob = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
        missing = sorted(set(need) - set(blob["source_layers"]))
        assert not missing, f"lens {ln} lacks layers {missing}"
        print(f"  lens {ln}: {path.name}, source layers {min(blob['source_layers'])}-{max(blob['source_layers'])} cover {need[0]}-{need[-1]}")
    assert max(need) <= pins.N_LAYERS - 2, "layer beyond the last lens source layer convention"
    # 4. arm mechanics on random tensors (CPU)
    mechanics_check()
    # 5. plan
    n_arms_full, n_arms_own = len(ARMS) + len(NULL_ARMS), len(OWN_PAIR_ARMS) + 2
    n_main = counts.get("primary", [0, 0])[1] + counts.get("side_table", [0, 0])[1]
    n_own = counts.get("own_pair_only", [0, 0])[1]
    nl = len(LENSES.get(target, ("jpp",)))
    print(f"  windows {[wname(s, e) for s, e, m in wins if not m]} + main band {wname(*MAIN_BAND[target])}")
    print(f"  upper bound (single-token items, before the greedy gate): {nl} lens(es) x {len(wins)} windows x "
          f"({n_main} items x {n_arms_full} rows + {n_own} items x {n_arms_own} rows) = "
          f"{nl * len(wins) * (n_main * n_arms_full + n_own * n_arms_own)} rows in {nl * len(wins) * (n_main + n_own)} batched forwards")


def mechanics_check(d: int = 96, seq: int = 7, seed: int = 0) -> None:
    """Each arm does what the docstring says, on random unit atoms and residuals."""
    g = torch.Generator().manual_seed(seed)
    unit = lambda *s: torch.nn.functional.normalize(torch.randn(*s, generator=g), dim=-1)  # noqa: E731
    h = torch.randn(seq, d, generator=g) * 3
    A = unit(12, d)
    B = unit(2, d) + 0.5 * A[:2]  # bridge atoms partly inside span(A), as a related category would be
    B = B / B.norm(dim=-1, keepdim=True)
    QA = basis(A)
    assert QA.shape[1] == 12 and torch.allclose(QA.T @ QA, torch.eye(12), atol=1e-5)
    layers = [5]
    clean = {5: h}
    Qs = {5: {"scrub": QA}}
    atoms = {("bridge", 5): B}
    atoms[("bridge_noA", 5)], _ = arm_atoms(B, QA, "orth")
    atoms[("bridge_onlyA", 5)], _ = arm_atoms(B, QA, "proj")
    e1, _ = build_edits("bridge", layers, atoms, clean, Qs, None)
    e3, _ = build_edits("bridge_noA", layers, atoms, clean, Qs, None)
    e4, _ = build_edits("bridge_noA_nm", layers, atoms, clean, Qs, None)
    e5, _ = build_edits("bridge_onlyA", layers, atoms, clean, Qs, None)
    en, _ = build_edits("bridge", layers, atoms, clean, Qs, 123)
    out1, out3, out4, out5, outn = (e[5](h) for e in (e1, e3, e4, e5, en))
    d1, d3, d4, d5, dn = (o - h for o in (out1, out3, out4, out5, outn))
    # arm 1: the clean coordinates on the two atoms exchanged at positions 1..; position 0 untouched
    P = torch.linalg.pinv(B)
    c0, c1 = h[1:] @ P, out1[1:] @ P
    assert torch.allclose(c1[:, 0], c0[:, 1], atol=1e-4) and torch.allclose(c1[:, 1], c0[:, 0], atol=1e-4)
    assert float(d1[0].norm()) == 0.0
    # arm 3: no component in span(A); arm 5: entirely in span(A)
    assert e3[5].share < 1e-8, e3[5].share
    assert abs(e5[5].share - 1) < 1e-5, e5[5].share
    assert e1[5].share > 1e-3  # the plain swap does put some of its edit in span(A) here
    # arm 4: arm 3's direction, arm 1's norm, per position
    assert torch.allclose(d4[1:].norm(dim=-1), d1[1:].norm(dim=-1), atol=1e-4)
    cos = torch.nn.functional.cosine_similarity(d4[1:], d3[1:], dim=-1)
    assert bool((cos > 0.9999).all())
    # null: arm 1's per-position norm along one random direction
    assert torch.allclose(dn[1:].norm(dim=-1), d1[1:].norm(dim=-1), atol=1e-4)
    assert float(torch.linalg.matrix_rank(dn[1:])) == 1
    # degenerate atoms are skipped, not divided by zero
    inside = A[:2]
    assert arm_atoms(inside, QA, "orth")[0] is None
    sk = build_edits("bridge_noA", layers, {("bridge_noA", 5): None}, clean, Qs, None)
    assert sk == ({}, [5])
    print("  mechanics: arm 1 swaps the coordinates (position 0 untouched); arm 3 edit share in span(A) "
          f"{e3[5].share:.1e}; arm 5 {e5[5].share:.6f}; arm 4 norm = arm 1's per position; null norm-matched, rank 1; "
          "degenerate atoms skipped: ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="CPU dry run (no model, no GPU)")
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=0, help="first K items (smoke)")
    ap.add_argument("--items", nargs="+", help="only these items (smoke)")
    ap.add_argument("--n-windows", type=int, default=0, help="only the first K cumulative windows (+ the main band; smoke)")
    ap.add_argument("--prompt-end", default="auto", choices=["auto", "stripped", "chat_prefill"])
    ap.add_argument("--repro-gate", action="store_true", help="27B: stop before the windows if arm 1 does not reproduce exp02")
    args = ap.parse_args()
    if args.check:
        check()
    else:
        assert args.name and args.why, "--name and --why"
        run(args)
