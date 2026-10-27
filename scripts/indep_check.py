"""indep_check: an independent re-implementation of X0's main test, to check what the pipeline computes.

Written from scratch on plain transformers + torch forward hooks, numpy and huggingface_hub; nothing is imported from
the project's package or from scripts/. It re-runs one stored X0 run (default: the 9B's, results/x0_necessity/
qwen35_9b_x0_necessity) on n random main-test items at one layer (default: the run's predicted layer) and compares,
per item x reader x arm, its own top token and logit difference with the stored ones.

What it computes, per item (one scene, two readers: lookup PP and recall PM, whose prompts agree through the bridge):
  prompts   the item's user turn "<context>\\n<question> Answer with a single digit and nothing else." in the model's
            chat template (thinking off), the assistant turn prefilled "Answer:"; tokenized without added special
            tokens (Qwen writes no BOS). org = the item's context, alt = its cf_context (two picks swap).
  position  the asked person's bridge word: the one token overlapping the bridge in "<holder> picked ... <bridge>."
            (holder = the "<name>'s pick" of the question); the same position in org and alt.
  delta     Δ = h_alt - h_org at that position, h = the output of decoder block L (fp32 from the bf16 residual), one
            unbatched forward per prompt.
  parts     the J++ part: Δ's k-atom signed OMP over unit J++ vectors of the letter-bearing tokens at L,
            v_t = unit((g * W_U[t]) @ J_L), g = the final RMSNorm's gain; the random part: Δ projected on the first
            m columns of a Haar-random orthonormal basis, m chosen per row so the projection keeps the J++ part's
            share of ||Δ||².
  arms      on the org prompt, at L and the bridge position, add Δ (whole), Δ - J++ part (no_part), Δ - random part
            (no_rand); the edit is h <- bf16(fp32(h) + x). An unedited row (none) is read beside them.
  read      one forward of the org prompt with the space token appended; the top token over the whole vocabulary
            of the last position's logits (no masking); role b (the alt answer's first token), A (the org's) or
            other; ld = logit(alt answer's first token) - logit(org's).
The stored outcomes keep the read's role, not the top token's id, so a stored "other" can only be compared as "other".

Verdict: PASS iff, on every arm (whole, no_part, no_rand), at least n - 1 items have both readers' roles agreeing with
the stored ones (19 of 20 by default); else FAIL. The unedited row, the ld differences, the J++ share against the
stored shares.jsonl and the prompt / position / answer-token matches against cases.jsonl are reported beside it.

Usage (GPU box):  uv run python scripts/indep_check.py --name <run> [--n 20] [--layer 12] [--device cuda]
Outputs: results/indep_check/<run>/ with manifest.json (written before any model is loaded), rows.jsonl, summary.json,
summary.md and prompts.md.
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import hashlib
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
STORED_RUN = REPO / "results" / "x0_necessity" / "qwen35_9b_x0_necessity"
ITEMS = REPO / "data" / "tasks_v2" / "d1_topics_v3" / "items.jsonl"
OUT_ROOT = REPO / "results" / "indep_check"
# Pins (src/bridge_jspace/pins.py TARGETS["qwen3.5-9b"]; the stored run's manifest.json repeats them)
MODEL_REPO = "Qwen/Qwen3.5-9B"
MODEL_REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
LENS_REPO = "neuronpedia/jacobian-lens"
LENS_FILE = "qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt"
LENS_REVISION = "e166deb5ad540932100ef803c8c9bcc2a5453694"
LENS_SHA256 = "8cda12f7ddf11e70fcfc69a47a9574f626fe084c67807a4781f4f67106e739c5"

READERS = ("PP", "PM")  # lookup, recall
ARMS = ("whole", "no_part", "no_rand")  # the rule's arms
READ_ARMS = ("none", *ARMS)  # rows of one read; "none" is descriptive
STORED_KEY = {"none": ("-", 0, "-"), "whole": ("-", 0, "-")}  # outcomes.jsonl's (dict, k, omp) per arm
K_ATOMS = 25
INSTRUCTION = "Answer with a single digit and nothing else."
PREFILL = "Answer:"
SELECT_SEED = 0
SUBSPACE_SEED = 888  # + layer, on the CPU (X0's documented convention; any seed gives a valid random part)
# Rows per read call in the stored run (x0_necessity.run_rendering, BJ_BATCH 64 > rows): at its predicted layer none,
# whole and 22 dictionary arms; elsewhere none, whole and 8. Padding to the same count keeps the GEMM shapes, so bf16
# rounding has a chance to match; each row's result does not depend on the other rows' content.
BATCH_ROWS = {"predicted": 24, "other": 10}
LETTER = re.compile(r"[^\W\d_]")  # a token is an atom iff its decode has a letter and it is not special
OPEN, CLOSE = "⟦", "⟧"


# ---- items and prompts (CPU) ------------------------------------------------------------------------------------


def read_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def stored_key(arm: str) -> tuple[str, int, str]:
    return STORED_KEY.get(arm, ("jpp", K_ATOMS, "signed"))


def select_scenes(rows: list[dict], layer: int, n: int, seed: int = SELECT_SEED, rendering: str = "chat") -> list[str]:
    """n scenes drawn with random.Random(seed).sample from the sorted scenes that have all three arms (whole, J++
    no_part and no_rand) for both readers at the layer."""
    have: dict[str, set] = collections.defaultdict(set)
    for r in rows:
        at = r["rendering"] == rendering and r["layer"] == layer and r["arm"] in ARMS
        if at and (r["dict"], r["k"], r["omp"]) == stored_key(r["arm"]):
            have[r["scene"]].add((r["reader"], r["arm"]))
    full = {(w, a) for w in READERS for a in ARMS}
    scenes = sorted(s for s, got in have.items() if got == full)
    if n > len(scenes):
        raise ValueError(f"{n} items asked, {len(scenes)} scenes have every arm at layer {layer}")
    return random.Random(seed).sample(scenes, n)


def holder_of(question: str) -> str:
    """The person whose pick the question asks about ('Which locker belongs to Iris's pick?' -> 'Iris')."""
    names = re.findall(r"\b(\w+)'s pick\b", question)
    if len(names) != 1:
        raise ValueError(f"no single '<name>'s pick' in {question!r}")
    return names[0]


def bridge_span(context: str, question: str, bridge: str) -> tuple[int, int]:
    """The character span of the bridge in the holder's pick sentence ('<holder> picked ... <bridge>.'), which must
    start the context or follow a sentence end, once."""
    holder = holder_of(question)
    starts = [m.start() for m in re.finditer(rf"(?:^|(?<=\. )){re.escape(holder)} picked ", context)]
    if len(starts) != 1:
        raise ValueError(f"{holder!r}'s pick sentence found {len(starts)} times in {context!r}")
    end = context.index(".", starts[0])
    i = context.rfind(bridge, starts[0], end)
    if i < 0 or context[i - 1] != " " or i + len(bridge) != end:
        raise ValueError(f"the bridge {bridge!r} does not end {holder!r}'s pick sentence")
    return i, i + len(bridge)


def render(tok, context: str, question: str) -> str:
    """One user turn in the chat template, thinking off, the assistant turn prefilled 'Answer:'."""
    msgs = [{"role": "user", "content": f"{context}\n{question} {INSTRUCTION}"}]
    text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    return text + PREFILL


def tokens_overlapping(offsets: list[tuple[int, int]], start: int, end: int) -> list[int]:
    return [i for i, (s, e) in enumerate(offsets) if e > s and s < end and e > start]


def encode(tok, text: str) -> tuple[list[int], list[tuple[int, int]]]:
    enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
    return list(enc["input_ids"]), [tuple(o) for o in enc["offset_mapping"]]


def first_token(tok, s: str) -> int:
    return tok(s, add_special_tokens=False)["input_ids"][0]


def build_case(tok, pp: dict, pm: dict) -> dict:
    """Both readers' org and alt prompts, the bridge position (one token, the same in all four prompts) and the answer
    tokens. Raises if the scene does not fit the design (the stored run dropped such scenes)."""
    for key in ("context", "cf_context", "bridge", "cf_bridge"):
        assert pp[key] == pm[key], f"{pp['scene']}: the readers' {key} differ"
    for it in (pp, pm):
        assert (it["format"], it["kind"]) == ("prose", "digit"), f"{it['id']}: only prose digit items are rendered"
    readers: dict[str, dict] = {}
    pos = None
    for w, it in (("PP", pp), ("PM", pm)):
        r: dict[str, Any] = {"id": it["id"], "question": it["question"], "answer": it["answer"],
                             "cf_answer": it["cf_answer"], "ids": {}, "text": {}, "offsets": {}}  # fmt: skip
        for v, context, bridge in (("org", it["context"], it["bridge"]), ("alt", it["cf_context"], it["cf_bridge"])):
            text = render(tok, context, it["question"])
            assert text.count(context) == 1, f"{it['id']}: the context is not once in the prompt"
            s, e = bridge_span(context, it["question"], bridge)
            base = text.index(context)
            ids, offsets = encode(tok, text)
            hit = tokens_overlapping(offsets, base + s, base + e)
            if len(hit) != 1:
                raise ValueError(f"{it['id']} {v}: the bridge {bridge!r} spans tokens {hit}")
            if pos is not None and hit[0] != pos:
                raise ValueError(f"{it['id']} {v}: bridge at {hit[0]}, elsewhere at {pos}")
            pos = hit[0]
            r["ids"][v], r["text"][v], r["offsets"][v] = ids, text, offsets
        if len(r["ids"]["org"]) != len(r["ids"]["alt"]) or r["ids"]["org"][pos] == r["ids"]["alt"][pos]:
            raise ValueError(f"{it['id']}: org and alt do not align at the bridge")
        r["tok_A"], r["tok_b"] = first_token(tok, it["answer"]), first_token(tok, it["cf_answer"])
        if r["tok_A"] == r["tok_b"]:
            raise ValueError(f"{it['id']}: the org and alt answers share their first token")
        readers[w] = r
    assert pos is not None
    for v in ("org", "alt"):
        if readers["PP"]["ids"][v][: pos + 1] != readers["PM"]["ids"][v][: pos + 1]:
            raise ValueError(f"{pp['scene']}: the readers' {v} prompts differ before the bridge")
    return {"scene": pp["scene"], "domain": pp["domain"], "bridge": pp["bridge"], "cf_bridge": pp["cf_bridge"],
            "context": pp["context"], "cf_context": pp["cf_context"], "pos": pos, "readers": readers}  # fmt: skip


def compare_case(mine: dict, stored: dict) -> dict:
    """Does the stored case (cases.jsonl) hold the same token ids, bridge position and answer tokens?"""
    ids = all(mine["readers"][w]["ids"][v] == stored["readers"][w]["ids"][v] for w in READERS for v in ("org", "alt"))
    answers = all(
        (mine["readers"][w]["tok_A"], mine["readers"][w]["tok_b"])
        == (stored["readers"][w]["tok_A"], stored["readers"][w]["tok_b"])
        for w in READERS
    )
    return {"ids": ids, "pos": mine["pos"] == stored["pos"], "answer_tokens": answers}


def mark(text: str, offsets: list[tuple[int, int]], pos: int) -> str:
    """The prompt text with the token at `pos` wrapped in ⟦ ⟧."""
    s, e = offsets[pos]
    return f"{text[:s]}{OPEN}{text[s:e]}{CLOSE}{text[e:]}"


# ---- parts (pure torch) -------------------------------------------------------------------------------------------


@torch.no_grad()
def signed_omp(atoms: torch.Tensor, x: torch.Tensor, k: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Orthogonal matching pursuit with signed coefficients, row by row of x [m, d] over unit atoms [n, d]: k times,
    take the unchosen atom with the largest |<residual, atom>|, then refit x by least squares on every chosen atom
    (float64); the residual is x minus that fit. Returns the fit [m, d] (fp32), the chosen atoms [m, k] in order and
    their coefficients [m, k]."""
    m = x.shape[0]
    x64 = x.double()
    resid = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    fit = torch.zeros_like(x64)
    coef = torch.zeros(m, 0, dtype=torch.float64, device=x.device)
    for _ in range(k):
        score = (resid @ atoms.T).abs()
        if chosen.shape[1]:
            score.scatter_(1, chosen, -1.0)
        chosen = torch.cat([chosen, score.argmax(dim=1, keepdim=True)], dim=1)
        a = atoms[chosen].double()  # [m, s, d]
        coef = torch.linalg.lstsq(a.transpose(1, 2), x64.unsqueeze(2)).solution.squeeze(2)  # [m, s]
        fit = (coef.unsqueeze(1) @ a).squeeze(1)
        resid = (x64 - fit).float()
    return fit.float(), chosen, coef


def haar_basis(d: int, seed: int) -> torch.Tensor:
    """A Haar-random orthonormal basis of R^d as the columns of [d, d] (QR of a CPU Gaussian, column signs fixed)."""
    q, r = torch.linalg.qr(torch.randn(d, d, generator=torch.Generator().manual_seed(seed)))
    return q * torch.sign(torch.diagonal(r))


def random_part(x: torch.Tensor, share: torch.Tensor, basis: torch.Tensor) -> torch.Tensor:
    """Each row of x [m, d] projected on the first m_row columns of `basis`, m_row the count whose projection's share
    of ||x_row||² is nearest share[row] (zero columns allowed)."""
    x = x.float()
    coord = x @ basis
    kept = torch.cumsum(coord**2, dim=1) / (x**2).sum(dim=1, keepdim=True).clamp_min(1e-30)
    kept = torch.cat([torch.zeros_like(kept[:, :1]), kept], dim=1)  # [m, d + 1]: share kept by 0..d columns
    count = (kept - share.float()[:, None]).abs().argmin(dim=1)
    use = torch.arange(basis.shape[1], device=x.device)[None, :] < count[:, None]
    return (coord * use) @ basis.T


def share_of(part: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    return (part.float() ** 2).sum(1) / (x.float() ** 2).sum(1).clamp_min(1e-30)


def role_of(top: int, tok_a: int, tok_b: int) -> str:
    return "b" if top == tok_b else "A" if top == tok_a else "other"


# ---- summary (CPU) ------------------------------------------------------------------------------------------------


def summarize(rows: list[dict], n: int, min_agree: int | None = None) -> dict:
    """Per arm: items whose two readers both agree with the stored role, rows agreeing, the switch counts and the
    largest |ld difference|; the verdict over the rule's arms."""
    need = n - 1 if min_agree is None else min_agree
    by_item: dict[tuple[str, str], list[bool]] = collections.defaultdict(list)
    out: dict[str, Any] = {"n_items": n, "min_items_agreeing": need, "arms": {}}
    for r in rows:
        by_item[(r["arm"], r["scene"])].append(r["agree"])
    for arm in READ_ARMS:
        mine = [r for r in rows if r["arm"] == arm]
        if not mine:
            continue
        items = [all(v) for (a, _), v in by_item.items() if a == arm]
        diffs = [abs(r["ld_diff"]) for r in mine if r["ld_diff"] is not None]
        out["arms"][arm] = {
            "items_agree": sum(items),
            "rows_agree": sum(r["agree"] for r in mine),
            "rows": len(mine),
            "switched_mine": {w: sum(r["my_role"] == "b" for r in mine if r["reader"] == w) for w in READERS},
            "switched_stored": {w: sum(r["stored_role"] == "b" for r in mine if r["reader"] == w) for w in READERS},
            "max_abs_ld_diff": max(diffs) if diffs else None,
            "mean_abs_ld_diff": round(float(np.mean(diffs)), 4) if diffs else None,
        }
    rule = [out["arms"].get(a, {}).get("items_agree", -1) for a in ARMS]
    out["verdict"] = "PASS" if all(v >= need for v in rule) else "FAIL"
    diffs = [abs(r["ld_diff"]) for r in rows if r["arm"] in ARMS and r["ld_diff"] is not None]
    out["max_abs_ld_diff"] = max(diffs) if diffs else None
    return out


# ---- model (GPU) --------------------------------------------------------------------------------------------------


def text_model(hf):
    """The text decoder (its layers and final norm): hf.model, or a multimodal model's hf.model.language_model."""
    return getattr(hf.model, "language_model", hf.model)


def load_model(repo: str, revision: str, dtype: torch.dtype, device: str):
    from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(repo, revision=revision)
    archs = AutoConfig.from_pretrained(repo, revision=revision).architectures or []
    auto = (
        AutoModelForImageTextToText
        if any(a.endswith("ForConditionalGeneration") for a in archs)
        else AutoModelForCausalLM
    )
    loaded: Any = auto.from_pretrained(repo, revision=revision, dtype=dtype, attn_implementation="sdpa",
                                       device_map=device, output_loading_info=True)  # fmt: skip
    hf, info = loaded
    missing = [k for k in info.get("missing_keys", []) if "mtp" not in k]
    assert not missing, f"{repo}: weights missing from the checkpoint: {missing[:5]}"
    return hf.eval(), tok


@contextlib.contextmanager
def hooked(module, fn):
    handle = module.register_forward_hook(fn)
    try:
        yield
    finally:
        handle.remove()


@torch.no_grad()
def block_output(hf, layer: int, ids: list[int], device: str, check_hidden: bool = False) -> tuple[torch.Tensor, float]:
    """The output of decoder block `layer` [seq, d] (fp32) for one unbatched prompt; with check_hidden also the
    largest |difference| from the model's own hidden_states[layer + 1] (the same tensor if the hook is right)."""
    got: dict[str, torch.Tensor] = {}

    def keep(_module, _args, out):
        got["h"] = (out[0] if isinstance(out, tuple) else out)[0].float().clone()

    with hooked(text_model(hf).layers[layer], keep):
        out = hf(input_ids=torch.tensor([ids], device=device), use_cache=False, logits_to_keep=1,
                 output_hidden_states=check_hidden)  # fmt: skip
    gap = float((out.hidden_states[layer + 1][0].float() - got["h"]).abs().max()) if check_hidden else float("nan")
    return got["h"], gap


@torch.no_grad()
def read_logits(hf, layer: int, ids: list[int], pos: int, adds: torch.Tensor, device: str) -> torch.Tensor:
    """Last-position logits [rows, vocab] (fp32) of one prompt read in a batch of len(adds) rows, row r with adds[r]
    added at (layer, pos) as bf16(fp32(h) + add); a zero row is the unedited prompt."""
    adds = adds.to(device)

    def patch(_module, _args, out):
        h = out[0] if isinstance(out, tuple) else out
        h = h.clone()
        h[:, pos] = (h[:, pos].float() + adds).to(h.dtype)
        return (h, *out[1:]) if isinstance(out, tuple) else h

    batch = torch.tensor([ids] * adds.shape[0], device=device)
    with hooked(text_model(hf).layers[layer], patch):
        out = hf(input_ids=batch, attention_mask=torch.ones_like(batch), use_cache=False, logits_to_keep=1)
    return out.logits[:, -1].float()


def norm_gain(hf, device: str) -> tuple[torch.Tensor, str]:
    """The final RMSNorm's per-dimension gain g (fp32): 1 + weight or weight, whichever reproduces the module on a
    random input."""
    norm = text_model(hf).norm
    w = norm.weight.float().to(device)
    x = torch.randn(4, w.shape[0], device=device, generator=torch.Generator(device=device).manual_seed(0))
    x = x.to(norm.weight.dtype)
    eps = getattr(norm, "eps", None) or getattr(norm, "variance_epsilon", 1e-6)
    base = x.float() * torch.rsqrt(x.float().pow(2).mean(-1, keepdim=True) + eps)
    y = norm(x).float()
    errs = {"one_plus_weight": (y - base * (1 + w)).abs().max(), "weight": (y - base * w).abs().max()}
    name = min(errs, key=lambda k: float(errs[k]))
    assert float(errs[name]) <= 0.02 * float(y.abs().max()), f"the final norm is neither x*(1+w) nor x*w: {errs}"
    return (1 + w if name == "one_plus_weight" else w), name


def letter_atoms(tok, vocab: int) -> list[int]:
    """Ids (of the lm_head's vocab) whose decode has a letter, special and added tokens excluded."""
    special = set(tok.all_special_ids) | {int(i) for i in tok.added_tokens_decoder}
    decoded = tok.batch_decode([[i] for i in range(vocab)])
    return [i for i, s in enumerate(decoded) if i not in special and LETTER.search(s)]


@torch.no_grad()
def lens_atoms(hf, j_layer: torch.Tensor, gain: torch.Tensor, ids: list[int], device: str, chunk: int = 32768):
    """Unit J++ vectors [len(ids), d] fp32: unit((g * W_U[t]) @ J_L)."""
    w_u = hf.get_output_embeddings().weight
    j = j_layer.to(device, torch.float32)
    out = torch.empty(len(ids), j.shape[0], device=device)
    index = torch.tensor(ids, device=w_u.device)
    for s in range(0, len(ids), chunk):
        rows = (w_u[index[s : s + chunk]].float().to(device) * gain) @ j
        out[s : s + chunk] = torch.nn.functional.normalize(rows, dim=-1)
    return out


def load_lens_layer(repo: str, file: str, revision: str, sha256: str | None, layer: int) -> tuple[torch.Tensor, dict]:
    from huggingface_hub import hf_hub_download

    path = Path(hf_hub_download(repo, file, revision=revision))
    got = sha256_file(path)
    if sha256 is not None:
        assert got == sha256, f"{file}: sha256 {got}, pinned {sha256}"
    blob = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
    assert layer in blob["source_layers"], f"{file}: no map at layer {layer} (has {blob['source_layers']})"
    meta = {"sha256": got, "source_layers": list(blob["source_layers"]), "d_model": blob.get("d_model"),
            "capture_point": (blob.get("provenance") or {}).get("capture_point")}  # fmt: skip
    return blob["J"][layer].float().clone(), meta


# ---- run ----------------------------------------------------------------------------------------------------------


def git_state() -> dict:
    def git(*a: str) -> str:
        return subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True, check=False).stdout.strip()

    return {"sha": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain")),
            "this_script_sha256": sha256_file(Path(__file__)),
            "this_script_tracked": bool(git("ls-files", str(Path(__file__).relative_to(REPO))))}  # fmt: skip


def stored_rows(rows: list[dict], scenes: set[str], layer: int) -> dict[tuple[str, str, str], dict]:
    out = {}
    for r in rows:
        at = r["scene"] in scenes and r["rendering"] == "chat" and r["layer"] == layer and r["arm"] in READ_ARMS
        if at and (r["dict"], r["k"], r["omp"]) == stored_key(r["arm"]):
            key = (r["scene"], r["reader"], r["arm"])
            assert key not in out, f"duplicate stored row {key}"
            out[key] = r
    return out


def check_pins(m: dict, a: argparse.Namespace) -> list[str]:
    """Where the CLI's model / lens differ from the stored run's manifest."""
    want = {"model repo": (m["model"]["repo"], a.model_repo), "model revision": (m["model"]["revision"], a.model_revision),
            "lens": (list(m["lens"]["source"]), [a.lens_repo, a.lens_file, a.lens_revision]),
            "lens sha256": (m["lens"]["sha256"], a.lens_sha256), "dtype": (m["model"]["dtype"], a.dtype),
            "prompt format": (m["model"].get("prompt_format"), "chat")}  # fmt: skip
    return [f"{k}: stored {s!r}, here {h!r}" for k, (s, h) in want.items() if s != h]


def run(a: argparse.Namespace) -> Path:
    import transformers
    from transformers import AutoTokenizer

    stored_dir = Path(a.stored_run)
    m = json.loads((stored_dir / "manifest.json").read_text())
    layer = m["predicted"] if a.layer is None else a.layer
    if a.batch_rows is None:
        a.batch_rows = BATCH_ROWS["predicted" if layer == m["predicted"] else "other"]
    assert a.batch_rows == 0 or a.batch_rows >= len(READ_ARMS), f"--batch-rows: 0 or >= {len(READ_ARMS)}"
    mismatches = check_pins(m, a)
    if mismatches and not a.allow_pin_mismatch:
        raise SystemExit(
            "pins differ from the stored run (pass --allow-pin-mismatch for a smoke test):\n  "
            + "\n  ".join(mismatches)
        )
    items_path = Path(a.items)
    items_sha = sha256_file(items_path)
    rel = str(items_path.resolve().relative_to(REPO)) if items_path.resolve().is_relative_to(REPO) else str(items_path)
    assert m["inputs"].get(rel) in (None, items_sha), (
        f"{rel}: sha256 {items_sha}, the stored run used {m['inputs'][rel]}"
    )

    outcomes = read_jsonl(stored_dir / "outcomes.jsonl")
    scenes = select_scenes(outcomes, layer, a.n, a.seed)
    stored = stored_rows(outcomes, set(scenes), layer)
    del outcomes
    stored_cases = {c["scene"]: c for c in read_jsonl(stored_dir / "cases.jsonl") if c["rendering"] == "chat"}
    stored_share = {s["scene"]: s for s in read_jsonl(stored_dir / "shares.jsonl")
                    if s["rendering"] == "chat" and s["layer"] == layer and (s["dict"], s["k"], s["omp"]) == ("jpp", K_ATOMS, "signed")}  # fmt: skip
    by_scene: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for it in read_jsonl(items_path):
        by_scene[it["scene"]][it["word"]] = it

    tok = AutoTokenizer.from_pretrained(a.model_repo, revision=a.model_revision)
    space = tok(" ", add_special_tokens=False)["input_ids"]
    assert len(space) == 1, f"the space is {space}, not one token"
    cases = [build_case(tok, by_scene[s]["PP"], by_scene[s]["PM"]) for s in scenes]
    matches = {c["scene"]: compare_case(c, stored_cases[c["scene"]]) for c in cases}

    out = Path(a.out_root) / a.name
    out.mkdir(parents=True, exist_ok=False)
    manifest = {
        "exp": "indep_check", "run": a.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "what": "independent re-implementation of X0's main test (whole / no_part / no_rand) on stored items",
        "stored_run": {"dir": str(stored_dir), "manifest_sha256": sha256_file(stored_dir / "manifest.json"),
                       "outcomes_sha256": sha256_file(stored_dir / "outcomes.jsonl")},
        "pins_match_stored": not mismatches, "pin_mismatches": mismatches,
        "model": {"repo": a.model_repo, "revision": a.model_revision, "dtype": a.dtype, "attn": "sdpa", "device": a.device},
        "lens": {"repo": a.lens_repo, "file": a.lens_file, "revision": a.lens_revision, "sha256_pinned": a.lens_sha256},
        "items_file": {"path": rel, "sha256": items_sha},
        "layer": layer, "k": K_ATOMS, "n": a.n,
        "selection": f"random.Random({a.seed}).sample(sorted scenes with whole, jpp/{K_ATOMS}/signed no_part and no_rand "
                     f"for both readers at chat layer {layer}, {a.n})",
        "items": scenes, "seeds": {"selection": a.seed, "random_subspace": f"{a.subspace_seed} + layer (CPU)"},
        "batch_rows": a.batch_rows, "code": git_state(), "argv": sys.argv,
        "env": {"torch": torch.__version__, "transformers": transformers.__version__,
                "gpu": torch.cuda.get_device_name() if torch.cuda.is_available() else None},
    }  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    from tqdm import tqdm

    dtype = {"bfloat16": torch.bfloat16, "float32": torch.float32}[a.dtype]
    dev = a.device
    hf, _ = load_model(a.model_repo, a.model_revision, dtype, dev)
    assert hf.get_input_embeddings().weight.device.type == torch.device(dev).type, "the model is not on --device"
    j_layer, lens_meta = load_lens_layer(a.lens_repo, a.lens_file, a.lens_revision, a.lens_sha256, layer)
    gain, gain_rule = norm_gain(hf, dev)
    vocab = hf.get_output_embeddings().weight.shape[0]
    letters = letter_atoms(tok, vocab)
    atoms = lens_atoms(hf, j_layer, gain, letters, dev)
    print(f"{len(letters)} letter atoms of {vocab}; norm gain {gain_rule}", flush=True)

    deltas, gaps = [], []
    for i, c in enumerate(tqdm(cases, desc="Δ at the bridge")):
        ids = c["readers"]["PP"]["ids"]
        h_org, gap = block_output(hf, layer, ids["org"], dev, check_hidden=i == 0)
        h_alt, _ = block_output(hf, layer, ids["alt"], dev)
        deltas.append(h_alt[c["pos"]] - h_org[c["pos"]])
        gaps.append(gap)
    x = torch.stack(deltas)  # [n, d] fp32
    part, chosen, _ = signed_omp(atoms, x, K_ATOMS)
    share = share_of(part, x)
    basis = haar_basis(x.shape[1], a.subspace_seed + layer).to(dev)
    rand = random_part(x, share, basis)
    rshare = share_of(rand, x)
    adds = {"none": torch.zeros_like(x), "whole": x, "no_part": x - part, "no_rand": x - rand}
    del atoms, basis

    rows, answers = [], {}
    for i, c in enumerate(tqdm(cases, desc="reads")):
        for w in READERS:
            rd = c["readers"][w]
            rows_add = torch.stack([adds[arm][i] for arm in READ_ARMS])
            if a.batch_rows > len(READ_ARMS):
                rows_add = torch.cat(
                    [rows_add, torch.zeros(a.batch_rows - len(READ_ARMS), x.shape[1], device=x.device)]
                )
            logits = read_logits(hf, layer, rd["ids"]["org"] + space, c["pos"], rows_add, dev)[: len(READ_ARMS)]
            probs = torch.softmax(logits, dim=-1)
            for j, arm in enumerate(READ_ARMS):
                lg, top = logits[j], int(logits[j].argmax())
                ld = float(lg[rd["tok_b"]] - lg[rd["tok_A"]])
                st = stored.get((c["scene"], w, arm))
                role = role_of(top, rd["tok_A"], rd["tok_b"])
                rows.append({
                    "scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": arm,
                    "my_top": top, "my_top_str": tok.decode([top]), "my_role": role,
                    "stored_role": st["role"] if st else None, "agree": bool(st) and role == st["role"],
                    "my_ld": round(ld, 4), "stored_ld": st["ld"] if st else None,
                    "ld_diff": round(ld - st["ld"], 4) if st else None,
                    "my_p_org": round(float(probs[j, rd["tok_A"]]), 4), "stored_p_org": st["p_org"] if st else None,
                    "my_p_alt": round(float(probs[j, rd["tok_b"]]), 4), "stored_p_alt": st["p_alt"] if st else None,
                })  # fmt: skip
                answers[(c["scene"], w, arm)] = rows[-1]

    write_outputs(out, a, cases, rows, answers, matches, share, rshare, stored_share, chosen, letters, tok, gaps,
                  lens_meta, gain_rule, len(letters), layer, mismatches)  # fmt: skip
    return out


def write_outputs(out, a, cases, rows, answers, matches, share, rshare, stored_share, chosen, letters, tok, gaps,
                  lens_meta, gain_rule, n_atoms, layer, mismatches) -> None:  # fmt: skip
    with (out / "rows.jsonl").open("w") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    share_rows = []
    for i, c in enumerate(cases):
        st = stored_share.get(c["scene"], {})
        share_rows.append({"scene": c["scene"], "my_share": round(float(share[i]), 5), "stored_share": st.get("share"),
                           "my_rand_share": round(float(rshare[i]), 5), "stored_rand_share": st.get("rand_share"),
                           "atoms": [tok.decode([letters[int(t)]]) for t in chosen[i][:5]]})  # fmt: skip
    summ = summarize(rows, len(cases))
    sd = [abs(r["my_share"] - r["stored_share"]) for r in share_rows if r["stored_share"] is not None]
    summ.update({
        "run": a.name, "layer": layer, "pins_match_stored": not mismatches, "pin_mismatches": mismatches,
        "prompts_match_stored": {k: sum(v[k] for v in matches.values()) for k in ("ids", "pos", "answer_tokens")},
        "share": {"max_abs_diff_vs_stored": max(sd) if sd else None,
                  "median_mine": float(np.median([r["my_share"] for r in share_rows])),
                  "max_abs_rand_minus_jpp": float((rshare - share).abs().max())},
        "hook_vs_hidden_states_max_abs": gaps[0], "norm_gain": gain_rule, "n_atoms": n_atoms, "lens": lens_meta,
        "items": share_rows,
    })  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summ, indent=2, ensure_ascii=False) + "\n")
    lines = [f"# indep_check {a.name}: {summ['verdict']}", "",
             f"Stored run `{a.stored_run}`, layer {layer}, chat, J++ k={K_ATOMS} signed OMP; n = {len(cases)} items "
             f"(random.Random({a.seed}).sample); rule: PASS iff every arm has >= {summ['min_items_agreeing']} items "
             "whose two readers both match the stored read's role (b / A / other).", ""]  # fmt: skip
    if mismatches:
        lines += ["**Pins differ from the stored run: a smoke test, not a check of it.** " + "; ".join(mismatches), ""]
    lines += ["| arm | items agree | rows agree | switched PP mine / stored | switched PM mine / stored | max abs ld diff | mean abs ld diff |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for arm, s in summ["arms"].items():
        lines.append(f"| {arm}{' (descriptive)' if arm == 'none' else ''} | {s['items_agree']}/{len(cases)} | "
                     f"{s['rows_agree']}/{s['rows']} | {s['switched_mine']['PP']} / {s['switched_stored']['PP']} | "
                     f"{s['switched_mine']['PM']} / {s['switched_stored']['PM']} | {s['max_abs_ld_diff']} | "
                     f"{s['mean_abs_ld_diff']} |")  # fmt: skip
    pm = summ["prompts_match_stored"]
    lines += ["", f"Prompts vs cases.jsonl: ids {pm['ids']}/{len(cases)}, bridge position {pm['pos']}/{len(cases)}, "
              f"answer tokens {pm['answer_tokens']}/{len(cases)}.",
              f"J++ share of ||Δ||²: median {summ['share']['median_mine']:.4f}; largest |mine - stored| "
              f"{summ['share']['max_abs_diff_vs_stored']}; random part's share off the J++ share by at most "
              f"{summ['share']['max_abs_rand_minus_jpp']:.2e}.",
              f"Hook (block {layer} output) vs hidden_states[{layer + 1}]: max |diff| {gaps[0]:.3g}. Final-norm gain: "
              f"{gain_rule}. Atoms: {n_atoms} letter tokens.", "",
              "Disagreements:", ""]  # fmt: skip
    bad = [r for r in rows if not r["agree"]]
    lines += [f"- {r['scene']} {r['reader']} {r['arm']}: mine {r['my_role']} ({r['my_top_str']!r}, ld {r['my_ld']}), "
              f"stored {r['stored_role']} (ld {r['stored_ld']})" for r in bad] or ["- none"]  # fmt: skip
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    space = tok(" ", add_special_tokens=False)["input_ids"]
    write_prompts(out / "prompts.md", cases[: a.n_prompts], answers, matches, space)


def write_prompts(path: Path, cases: list[dict], answers: dict, matches: dict, space: list[int]) -> None:
    lines = ["# Prompts as the model reads them", "",
             f"The org prompt of each reader, chat template applied, the patched token in {OPEN} {CLOSE}. The read "
             f"appends the space token (id {space[0]}, ' ') after 'Answer:' and takes the top token over the "
             "vocabulary. b = the alt answer's first token, A = the org answer's, other = neither. 'mine' is this "
             "check's read; 'stored' is outcomes.jsonl's role and ld.", ""]  # fmt: skip
    for n, c in enumerate(cases, 1):
        pp = c["readers"]["PP"]
        tok_text = pp["text"]["org"][slice(*pp["offsets"]["org"][c["pos"]])]
        alt_tok = pp["text"]["alt"][slice(*pp["offsets"]["alt"][c["pos"]])]
        lines += [f"## {n}. {c['scene']} ({c['domain']}): {c['bridge']} -> {c['cf_bridge']}", "",
                  f"Patched position {c['pos']}: org token {tok_text!r} (id {pp['ids']['org'][c['pos']]}), alt token "
                  f"{alt_tok!r} (id {pp['ids']['alt'][c['pos']]}). Matches cases.jsonl: {matches[c['scene']]}.", "",
                  f"Alt context (Δ's source): {c['cf_context']}", ""]  # fmt: skip
        for w in READERS:
            rd = c["readers"][w]
            lines += [f"**{w}** ({'lookup' if w == 'PP' else 'recall'}): org answer {rd['answer']}, alt answer "
                      f"{rd['cf_answer']}", "", "```text", mark(rd["text"]["org"], rd["offsets"]["org"], c["pos"]),
                      "```", ""]  # fmt: skip
        lines += ["| arm | PP: mine | PP: stored | PM: mine | PM: stored |", "|---|---|---|---|---|"]
        for arm in READ_ARMS:
            cells = []
            for w in READERS:
                r = answers[(c["scene"], w, arm)]
                cells += [f"{r['my_top_str']!r} ({r['my_role']}, ld {r['my_ld']:+.3f})",
                          f"{r['stored_role']} (ld {r['stored_ld']:+.3f})" if r["stored_role"] else "-"]  # fmt: skip
            lines.append(f"| {arm} | " + " | ".join(cells) + " |")
        lines.append("")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="run name: results/indep_check/<name>/ (new)")
    ap.add_argument("--n", type=int, default=20, help="items")
    ap.add_argument("--layer", type=int, default=None, help="default: the stored run's predicted layer")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default="bfloat16", choices=["bfloat16", "float32"])
    ap.add_argument("--seed", type=int, default=SELECT_SEED, help="item selection: random.Random(seed).sample")
    ap.add_argument("--subspace-seed", type=int, default=SUBSPACE_SEED, help="the random basis's seed is this + layer")
    ap.add_argument("--batch-rows", type=int, default=None,
                    help="rows per read call, padded with unedited rows; 0: no padding (default: the stored run's "
                         "count, 24 at its predicted layer, 10 elsewhere)")  # fmt: skip
    ap.add_argument("--n-prompts", type=int, default=10, help="items written to prompts.md")
    ap.add_argument("--stored-run", default=str(STORED_RUN))
    ap.add_argument("--items", default=str(ITEMS))
    ap.add_argument("--out-root", default=str(OUT_ROOT))
    ap.add_argument("--model-repo", default=MODEL_REPO)
    ap.add_argument("--model-revision", default=MODEL_REVISION)
    ap.add_argument("--lens-repo", default=LENS_REPO)
    ap.add_argument("--lens-file", default=LENS_FILE)
    ap.add_argument("--lens-revision", default=LENS_REVISION)
    ap.add_argument("--lens-sha256", default=LENS_SHA256, help="'none' skips the check (smoke tests only)")
    ap.add_argument("--allow-pin-mismatch", action="store_true", help="smoke test with another model or lens")
    a = ap.parse_args()
    a.lens_sha256 = None if a.lens_sha256 == "none" else a.lens_sha256
    out = run(a)
    # batch 45: a FAIL exits non-zero, so the queue blocks every job that depends on this check (Dan ~18:25)
    verdict = json.loads((out / "summary.json").read_text())["verdict"]
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
