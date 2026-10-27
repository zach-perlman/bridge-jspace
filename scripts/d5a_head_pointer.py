"""d5a_head_pointer (Dan's D5a, task b; 2026-10-21): does the late lookup head follow the POINTER?

Background (UNVERIFIED). d2_lookup_heads: on unedited pointer_v1 scenes, attention from the last token of layer 51,
query head 22 falls most on the asked statement in 100% of held-out scenes, but also in 95% of recall questions
(memory → memory), where the statement is not needed: it locates the bridge's statement. pointer_swap (D3): patching
the alt prompt's last tokens / tokens after the question at layers 48 or 50 into the org prompt moves the answer to
another statement of the org prompt (the statement at the alt prompt's slot, or the alt entity's), item by item.

Question. After such a patch, which statement does the head attend to most: the one the new answer comes from (it
follows the pointer), or still the org prompt's asked statement (it tracks something the patch did not change)? And
is that read better than the J-lens's word read on the same tokens?

Items. pointer_v4 main (countries, animals, body; 85 queried entities, 9 wordings), the scenes of d3v4_swap_main
(pointer_swap's sample: eligible in every family, seed 0, n per topic), families memory → prompt (RL, primary),
named → prompt (DL, reference), memory → memory (RR, the recall control: no lookup).
Edits (pointer_swap's, unchanged): the org prompt's block output at the positions of a group replaced by a source
prompt's (token-aligned) at ONE layer: groups last (the read's last two tokens) and final (every token after the
question), layers 48 and 50 (64 layers; the same depth fractions elsewhere). Sources: dissoc (the alt prompt: bridge
alt at the slot where the org prompt has another entity), same (the same entity at the same slot, the rest
reshuffled: no answer should move), rand (a random direction of the dissoc patch's per-position norm, added). One
forward per item (unedited + 3 sources x 2 groups x 2 layers = 13 rows).
Read-outs per row: the answer (suite_split's read: top token at the answer's first token; pointer_swap's role map);
for each listed head (default HEADS: layer 51 head 22 first, then the 4 next late heads by the same read-out on
d2_lookup_heads, pointer_v1 scenes, held out from these), the attention from the last token summed over each org
statement's tokens, recomputed from the edited forward's own layer inputs (bridge_jspace.knockout.capture_attention);
the J-lens (the frozen lens) at the last token at the block before the first head's layer (layer 50: what layer 51
reads), its logits over the five entities' tokens.
Outcome per row: kept (role none: the org statement), slot (position), word (identity: the alt entity's statement),
other statement (context: another org digit), off the prompt (value, recall, other; no statement). Moved = slot, word
or other statement; its "new statement" is the org statement holding the new answer. Memory → memory: moved =
identity (the alt entity's recalled fact), its new statement = the alt entity's statement (where the bridge now is).

Decision rule (fixed before the run; job spec jobs/d5/d5a_head_pointer_27b.yaml). Primary cut: memory → prompt,
source dissoc, the four patch settings pooled; unit a row; intervals by entity cluster (queried entity resampled
within topic, 4000 draws, seed 0; stats.cluster_bootstrap), item-level Wilson second; n rows / k entities / t
wordings per cell; a cut is judged only with >= 35 rows.
  H-head-follows (layer 51 head 22): on moved rows the head's top statement is the new statement with lower bound
    >= 60%, AND on unmoved rows (kept) it is the org statement with lower bound >= 80%.
  H-head-static: on moved rows the head's top statement is the org statement with lower bound >= 60%.
  Otherwise neither (reported with the shares). The J-lens comparison: on the same moved rows, the share where the
  lens's top entity's statement is the new statement; paired difference head - lens (entity cluster); the head reads
  the pointer better than the lens iff its lower bound > 0.
  Controls: the same-entity patch and the random push should move <= 10% of answers and leave the head on the org
  statement (>= 80%); memory → memory: reported (does the head move to the bridge's new statement without a lookup?).
  The other heads get the same numbers, not a verdict.

Stages (write-once; the manifest is written before the run):
  manifest --name N --why W [--n 150] [--families RL DL RR] [--domains ..] [--heads 51:22 ...] [--no-lens]
           [--competence d3v4_competence_27b | --no-eligibility]
  run --name N          check.json, rows.jsonl
  summarise --name N    analysis-<UTC stamp>/summary.json, summary.md
  examples --name N [--k 3]   examples.json (job-page schema)
  figures --name N      analysis-<stamp>-figures/ (figures, summary.json, report.md; replaces the previous one)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import shutil
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
from bridge_jspace.knockout import FULL, capture_attention, decoder_layers, layer_kind
from bridge_jspace.stats import cluster_bootstrap, paired_bootstrap_diff, wilson
from scripts import pointer_swap as PS
from scripts import pointer_v4 as PV4
from scripts import suite_v1 as S

EXP = "d5a_head_pointer"
RESULTS = Path(os.environ.get("BJ_D5A_RESULTS", str(pins.RESULTS_DIR / EXP)))
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Chosen on d2_lookup_heads (pointer_v1, held out from pointer_v4): share of org prompts (memory → prompt and named →
# prompt) whose last-token attention is largest on the asked statement, ties by its mean share (UNVERIFIED):
# 51:22 100% (share 90%), 59:3 100% (89%), 59:1 99% (74%), 55:23 99% (73%), 59:21 98.5% (76%).
HEADS = ("51:22", "59:3", "59:1", "55:23", "59:21")
PATCH_DEPTH = (48, 50)  # of 64 layers
GROUPS = ("last", "final")
SOURCES = ("dissoc", "same", "rand")
FOLLOW_MOVED, FOLLOW_STAY, STATIC_MOVED, CONTROL_MOVED, MIN_N = 0.60, 0.80, 0.60, 0.10, 35
N_BOOT, BOOT_SEED, NULL_SEED, EXAMPLE_SEED = 4000, 0, 0, 0
MOVED = ("slot", "word", "other statement")
OUTCOME = {"none": "kept", "position": "slot", "identity": "word", "context": "other statement"}
FAMILY_WORDS = {"RL": "memory → prompt", "DL": "named → prompt", "RR": "memory → memory"}


def patch_layers(n_layers: int) -> list[int]:
    """Layers 48 and 50 of 64; the same depth fractions in another model (distinct layers)."""
    out = sorted({round(d * n_layers / 64) for d in PATCH_DEPTH})
    assert len(out) == len(PATCH_DEPTH), f"patch layers collide at {n_layers} layers"
    return out


def parse_heads(specs: list[str]) -> list[tuple[int, int]]:
    return [(int(s.split(":")[0]), int(s.split(":")[1])) for s in specs]


# ---- items ----------------------------------------------------------------------------------------------------------


def statement_tokens(prep: dict, item: dict) -> list[list[int]]:
    """Token positions of each org statement (slot order) in the rendered org prompt."""
    text, offsets, out, start = prep["text"], prep["offsets"], [], 0
    for stmt in item["statements"]:
        a = text.index(stmt, start)
        b = a + len(stmt)
        toks = [i for i, (s, e) in enumerate(offsets) if e > s and s < b and e > a]
        assert toks, f"{item['id']}: no tokens for {stmt!r}"
        out.append(toks)
        start = b
    return out


def entity_tokens(tok, item: dict) -> list[int] | None:
    """Each entity's single token (with its leading space), or None if one is not a single token or two coincide."""
    ids = [S.ids(tok, " " + e) for e in item["entities"]]
    if any(len(x) != 1 for x in ids) or len({x[0] for x in ids}) != len(ids):
        return None
    return [x[0] for x in ids]


def answer_statement(item: dict, digit: str | None, role: str) -> int | None:
    """The org statement a row's answer comes from: kept -> the asked statement; a lookup's moved answer -> the org
    statement holding that digit; memory → memory's identity -> the alt entity's statement (the bridge moved there)."""
    if role == "none":
        return item["slots"]["query"]
    if item["family"] == "RR":
        return item["slots"]["identity"] if role == "identity" else None
    if role in ("position", "identity", "context") and digit is not None and int(digit) in item["digits"]:
        return item["digits"].index(int(digit))
    return None


def outcome_of(item: dict, role: str) -> str:
    if item["family"] == "RR":
        return {"none": "kept", "identity": "word"}.get(role, "off the prompt")
    return OUTCOME.get(role, "off the prompt")


def run_manifest_items(m: dict) -> dict:
    """pointer_swap's view of this run's items (its sample_cases picks the scenes: d3v4_swap_main's for the same n)."""
    return {"data": "pointer_v4", "set": "main", "families": m["families"], "domains": m["domains"],
            "levels": [PV4.LEVEL], "n": m["n"], "competence": m["competence"],
            "competence_path": m["competence_path"], "items": m["items"]}  # fmt: skip


# ---- model ----------------------------------------------------------------------------------------------------------


def load_target() -> Any:
    """Part B's loader (bf16, CUDA); without a GPU (a local smoke on the 0.8B) the text model in fp32 on CPU."""
    if DEVICE == "cuda":
        from bridge_jspace.model import load_model

        return load_model()
    from types import SimpleNamespace

    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM

    from bridge_jspace.tokens import load_tokenizer

    path = snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True)
    hf = AutoModelForCausalLM.from_pretrained(path, dtype=torch.float32, attn_implementation="sdpa").eval()
    return SimpleNamespace(hf=hf, tokenizer=load_tokenizer())


class Lens:
    """The frozen J-lens at one layer: logits = unembed(h @ J_l.T). On CUDA bridge_jspace.lens.JLens (sha-checked);
    on CPU (a smoke) the same file read directly."""

    def __init__(self, model: Any, layer: int):
        self.layer = layer
        if DEVICE == "cuda":
            from bridge_jspace.lens import JLens

            self.jlens: Any = JLens(model, pins.FROZEN_LENS)
            assert layer in self.jlens.source_layers, f"the lens has no layer {layer}"
            return
        from huggingface_hub import hf_hub_download

        repo, file, revision = pins.LENS_SOURCES[pins.FROZEN_LENS]
        blob = torch.load(hf_hub_download(repo, file, revision=revision), map_location="cpu", weights_only=True)
        assert layer in list(blob["source_layers"]), f"the lens has no layer {layer}"
        self.jlens, self.J, self.hf = None, blob["J"][layer].float(), model.hf

    @torch.no_grad()
    def logits(self, h: torch.Tensor) -> torch.Tensor:
        if self.jlens is not None:
            return self.jlens.readout(h, self.layer)
        text = getattr(self.hf.model, "language_model", self.hf.model)
        return self.hf.lm_head(text.norm(h.float() @ self.J.T)).float()


@torch.no_grad()
def block_outputs(hf: Any, rows: list[list[int]], layers: list[int]) -> dict[int, torch.Tensor]:
    """Block outputs [rows, T, d] (fp32) at `layers` of a batch of token-aligned prompts."""
    blocks: Any = decoder_layers(hf)
    out: dict[int, torch.Tensor] = {}

    def hook_for(la: int):
        def hook(_m, _a, o):
            out[la] = (o[0] if isinstance(o, tuple) else o).float().clone()

        return hook

    handles = [blocks[la].register_forward_hook(hook_for(la)) for la in layers]
    try:
        hf(input_ids=torch.tensor(rows, device=DEVICE), use_cache=False, logits_to_keep=1)
    finally:
        for h in handles:
            h.remove()
    return out


@torch.no_grad()
def patched_forward(hf: Any, ids: list[int], edits: list[dict[int, Any]], att_layers: list[int],
                    lens_layer: int | None) -> tuple[torch.Tensor, dict[int, torch.Tensor], torch.Tensor | None]:  # fmt: skip
    """One batched forward of the org prompt, one row per edit set ({layer: edit of [T, d]}; pointer_swap's SetRows /
    AddRows): last-position logits [rows, vocab], the attention from the last token at att_layers
    {layer: [rows, heads, 1, T]} and the block output at lens_layer at the last position [rows, d] (after any edit)."""
    blocks: Any = decoder_layers(hf)
    rec: dict[str, torch.Tensor] = {}

    def hook_for(la: int):
        def hook(_m, _a, o):
            h = o[0] if isinstance(o, tuple) else o
            edited = any(la in e for e in edits)
            if edited:
                h = h.clone()
                for r, e in enumerate(edits):
                    if la in e:
                        h[r] = e[la](h[r].float()).to(h.dtype)
            if la == lens_layer:
                rec["h"] = h[:, -1].float().clone()
            if not edited:
                return None
            return (h, *o[1:]) if isinstance(o, tuple) else h

        return hook

    layers = sorted({la for e in edits for la in e} | ({lens_layer} if lens_layer is not None else set()))
    handles = [blocks[la].register_forward_hook(hook_for(la)) for la in layers]
    probs: dict[int, torch.Tensor] = {}
    try:
        with capture_attention(hf, att_layers, [len(ids) - 1], probs):
            batch = torch.tensor([ids] * len(edits), device=DEVICE)
            logits = hf(input_ids=batch, use_cache=False, logits_to_keep=1).logits[:, -1].float()
    finally:
        for h in handles:
            h.remove()
    return logits, probs, rec.get("h")


# ---- stages ---------------------------------------------------------------------------------------------------------


def stage_manifest(args) -> None:
    pins.check_run_name(args.name)
    path = RESULTS / args.name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    families = args.families
    domains = args.domains or list(PV4.DOMAINS)
    files = {lab: f for lab, f in PV4.set_files("main").items()
             if lab.split("_")[0] in domains and lab.split("_")[1] in families and f.exists()}  # fmt: skip
    assert files, "no pointer_v4 files for these families and domains"
    assert args.competence or args.no_eligibility, "--competence RUN (or --no-eligibility for a smoke)"
    comp = PV4.RESULTS / args.competence / "items.jsonl" if args.competence else None
    root = pins.REPO_ROOT
    m = {
        "exp": EXP, "run": args.name, "why": args.why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": pins.model_pin(), "data": "pointer_v4", "families": families, "domains": domains, "n": args.n,
        "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                  for k, f in files.items()},
        "competence": args.competence,
        "competence_path": str(comp.relative_to(root)) if comp else None,
        "competence_sha256": sha256_of(comp) if comp else None,
        "heads": args.heads, "groups": list(GROUPS), "sources": list(SOURCES), "lens": not args.no_lens,
        "patch_depth_of_64": list(PATCH_DEPTH),
        "sample": "pointer_swap.sample_cases (seed 0): per topic up to n scenes eligible in every family; with n=150 "
        "and d3v4_competence_27b the scenes of d3v4_swap_main",
        "seeds": {"sample": PS.SAMPLE_SEED, "null": NULL_SEED, "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
        "decision": (__doc__ or "").split("Decision rule")[1].split("Stages")[0].strip(),
        "thresholds": {"follow_moved": FOLLOW_MOVED, "follow_stay": FOLLOW_STAY, "static_moved": STATIC_MOVED,
                       "control_moved": CONTROL_MOVED, "min_n": MIN_N, "n_boot": N_BOOT},
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "rows.jsonl").exists(), f"{out_dir} has results; runs are written once"
    chat.check_format(m)
    for pin in m["items"].values():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{pin['file']} changed since the manifest"
    if m["competence_path"]:
        assert sha256_of(pins.REPO_ROOT / m["competence_path"]) == m["competence_sha256"], "competence run changed"
    model = load_target()
    hf, tok = model.hf, model.tokenizer
    blocks: Any = decoder_layers(hf)
    n_layers = len(blocks)
    p_layers = patch_layers(n_layers)
    heads = parse_heads(m["heads"])
    att_layers = sorted({la for la, _ in heads})
    assert all(layer_kind(blocks[la]) == FULL for la in att_layers), "a listed head is not in a full-attention layer"
    assert max(p_layers) < min(att_layers), "the patch must come before the heads read"
    lens_layer = min(att_layers) - 1
    lens = Lens(model, lens_layer) if m["lens"] else None
    t0 = time.time()
    pm = run_manifest_items(m)
    cases, counts = PS.sample_cases(pm, PS.load_items(pm))
    print(json.dumps(counts), flush=True)
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    rows: list[dict] = []
    check: dict[str, Any] = {"patch_layers": p_layers, "att_layers": att_layers, "lens_layer": lens_layer,
                             "heads": m["heads"], "counts": counts, "no_entity_tokens": 0, "self_patch_max_abs": 0.0}  # fmt: skip
    for ci, c in enumerate(progress(cases, "items")):
        prep = PS.prepare(c, tok)
        stmts = statement_tokens(prep, c)
        ents = entity_tokens(tok, c)
        check["no_entity_tokens"] += ents is None
        ids = prep["read_ids"]
        src = block_outputs(hf, [ids["base"], ids["dissoc"], ids["same"]], p_layers)
        gen = torch.Generator(device=DEVICE).manual_seed(NULL_SEED + 7919 * ci)
        specs: list[tuple[dict, dict]] = [({"source": "unedited", "group": "-", "layer": -1}, {}),
                                          ({"source": "self", "group": "last", "layer": p_layers[0]},
                                           {p_layers[0]: PS.SetRows(src[p_layers[0]][0][prep["groups"]["last"]],
                                                                    prep["groups"]["last"])})]  # fmt: skip
        for la in p_layers:
            for grp in GROUPS:
                pos = prep["groups"][grp]
                delta = src[la][1][pos] - src[la][0][pos]
                specs += [({"source": "dissoc", "group": grp, "layer": la}, {la: PS.SetRows(src[la][1][pos], pos)}),
                          ({"source": "same", "group": grp, "layer": la}, {la: PS.SetRows(src[la][2][pos], pos)}),
                          ({"source": "rand", "group": grp, "layer": la}, {la: PS.AddRows(PS.null_rows(delta, gen), pos)})]  # fmt: skip
        logits, probs, h_lens = patched_forward(hf, ids["base"], [e for _, e in specs], att_layers,
                                                lens_layer if lens else None)  # fmt: skip
        check["self_patch_max_abs"] = max(check["self_patch_max_abs"], float((logits[1] - logits[0]).abs().max()))
        lookup = c["family"] != "RR"
        roles = PS.role_map(c, c["sources"]["dissoc"]["predictions"], lookup)
        lens_ent = lens.logits(h_lens)[:, ents].float() if lens is not None and ents is not None and h_lens is not None else None  # fmt: skip
        for r, (tags, _) in enumerate(specs):
            if tags["source"] == "self":
                continue
            top = int(logits[r].argmax())
            digit = digit_tok.get(top)
            role = roles.get(digit, "other_digit") if digit is not None else "other"
            reads: dict[str, Any] = {}
            for la, h in heads:
                p = probs[la][r, h, 0]
                masses = [float(p[s].sum()) for s in stmts]
                reads[f"{la}:{h}"] = {"top": max(range(len(masses)), key=lambda i, ms=masses: ms[i]),
                                      "masses": [round(x, 4) for x in masses]}  # fmt: skip
            lens_read = None
            if lens_ent is not None:
                v = lens_ent[r].tolist()
                lens_read = {"top": max(range(len(v)), key=lambda i, v=v: v[i]), "logits": [round(x, 3) for x in v]}
            rows.append({"id": c["id"], "family": c["family"], "domain": c["domain"], "entity": c["query"],
                         "scene": c["scene"], **PS.wording_of(c), **tags, "top": tok.decode([top]), "digit": digit,
                         "role": role, "outcome": outcome_of(c, role), "org_statement": c["slots"]["query"],
                         "new_statement": answer_statement(c, digit, role), "heads": reads, "lens": lens_read})  # fmt: skip
    check["seconds"] = round(time.time() - t0, 1)
    check["rows"] = len(rows)
    check["items"] = len(cases)
    check["self_patch_noop"] = (
        check["self_patch_max_abs"] < 1e-3 if DEVICE == "cpu" else check["self_patch_max_abs"] < 0.5
    )
    write_jsonl(out_dir / "rows.jsonl", rows)
    write_jsonl(out_dir / "cases.jsonl", [{"id": c["id"], "family": c["family"], "domain": c["domain"],
                                           "entity": c["query"], "scene": c["scene"]} for c in cases])  # fmt: skip
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    print(json.dumps({k: v for k, v in check.items() if k != "counts"}), flush=True)


# ---- analysis (CPU, saved rows only) -------------------------------------------------------------------------------


def share(rows: list[dict], hit) -> dict:
    """Share of rows where hit(row) holds: entity-cluster interval (queried entity within topic) first, Wilson second;
    n rows / k entities / t wordings; per topic."""
    if not rows:
        return {"n": 0}
    v = [float(bool(hit(r))) for r in rows]
    ents, doms = [r["entity"] for r in rows], [r["domain"] for r in rows]
    cl = cluster_bootstrap(v, ents, doms, n_boot=N_BOOT, seed=BOOT_SEED)
    per = {d: {"n": doms.count(d), "share": statistics.mean(x for x, dd in zip(v, doms, strict=True) if dd == d)}
           for d in sorted(set(doms))}  # fmt: skip
    return {"n": len(v), "k": len(set(zip(doms, ents, strict=True))), "t": len({r.get("template") for r in rows}),
            "share": cl[0], "cluster": [cl[1], cl[2]], "wilson": list(wilson(int(sum(v)), len(v))[1:]), "per_topic": per}  # fmt: skip


def reader_top(r: dict, reader: str) -> int | None:
    if reader == "lens":
        return r["lens"]["top"] if r.get("lens") else None
    return r["heads"][reader]["top"]


def reader_scores(rows: list[dict], reader: str) -> dict:
    """On moved rows: names the new statement / the org statement; on kept rows: the org statement."""
    rs = [r for r in rows if reader_top(r, reader) is not None]
    moved = [r for r in rs if r["outcome"] in MOVED and r["new_statement"] is not None]
    kept = [r for r in rs if r["outcome"] == "kept"]
    return {"moved_new": share(moved, lambda r: reader_top(r, reader) == r["new_statement"]),
            "moved_org": share(moved, lambda r: reader_top(r, reader) == r["org_statement"]),
            "kept_org": share(kept, lambda r: reader_top(r, reader) == r["org_statement"])}  # fmt: skip


def paired_vs_lens(rows: list[dict], head: str) -> dict:
    moved = [r for r in rows if r["outcome"] in MOVED and r["new_statement"] is not None and r.get("lens")]
    if not moved:
        return {"n": 0}
    d = [
        float(reader_top(r, head) == r["new_statement"]) - float(reader_top(r, "lens") == r["new_statement"])
        for r in moved
    ]
    cl = cluster_bootstrap(d, [r["entity"] for r in moved], [r["domain"] for r in moved], n_boot=N_BOOT, seed=BOOT_SEED)
    hits = [float(reader_top(r, head) == r["new_statement"]) for r in moved]
    lens_hits = [float(reader_top(r, "lens") == r["new_statement"]) for r in moved]
    it = paired_bootstrap_diff(hits, lens_hits, 2000, BOOT_SEED)
    return {"n": len(d), "diff": cl[0], "cluster": [cl[1], cl[2]], "items": [it[1], it[2]], "head_better": cl[1] > 0}


def verdicts(sc: dict) -> dict:
    """H-head-follows / H-head-static on a reader's primary scores (the rule in the docstring)."""
    mn, mo, ko = sc["moved_new"], sc["moved_org"], sc["kept_org"]
    if mn.get("n", 0) < MIN_N or ko.get("n", 0) < MIN_N:
        return {"follows": None, "static": None, "verdict": f"not judged (moved n={mn.get('n', 0)}, kept n={ko.get('n', 0)} < {MIN_N})"}  # fmt: skip
    follows = mn["cluster"][0] >= FOLLOW_MOVED and ko["cluster"][0] >= FOLLOW_STAY
    static = mo["cluster"][0] >= STATIC_MOVED
    return {"follows": follows, "static": static,
            "verdict": "follows the pointer" if follows else "static" if static else "neither"}  # fmt: skip


def analyse(m: dict, rows: list[dict]) -> dict:
    readers = [*m["heads"], *(["lens"] if m["lens"] else [])]
    out: dict[str, Any] = {"cells": {}, "settings": {}, "controls": {}, "outcomes": {}}
    for fam in m["families"]:
        dis = [r for r in rows if r["family"] == fam and r["source"] == "dissoc"]
        out["cells"][fam] = {rd: reader_scores(dis, rd) for rd in readers}
        out["outcomes"][fam] = dict(collections.Counter(r["outcome"] for r in dis))
        for grp in GROUPS:
            for la in sorted({r["layer"] for r in dis}):
                sel = [r for r in dis if r["group"] == grp and r["layer"] == la]
                out["settings"][f"{fam}|{grp}|{la}"] = {
                    "moved": share(sel, lambda r: r["outcome"] in MOVED),
                    "head": reader_scores(sel, m["heads"][0])}  # fmt: skip
        for kind in MOVED:
            sel = [r for r in dis if r["outcome"] == kind]
            out["outcomes"][f"{fam}|{kind}"] = {rd: share(sel, lambda r, rd=rd: reader_top(r, rd) == r["new_statement"])
                                                for rd in readers}  # fmt: skip
        for src in ("same", "rand", "unedited"):
            sel = [r for r in rows if r["family"] == fam and r["source"] == src]
            out["controls"][f"{fam}|{src}"] = {
                "moved": share(sel, lambda r: r["outcome"] != "kept"),
                "head_org": share(sel, lambda r: reader_top(r, m["heads"][0]) == r["org_statement"])}  # fmt: skip
        if m["lens"]:
            out["cells"][fam]["paired_vs_lens"] = paired_vs_lens(dis, m["heads"][0])
    prim = out["cells"].get("RL", {}).get(m["heads"][0])
    out["primary"] = verdicts(prim) if prim else {"verdict": "no memory → prompt rows"}
    out["controls_ok"] = {f"{f}|{s}": (c["moved"].get("share", 1) <= CONTROL_MOVED)
                          for k, c in out["controls"].items() for f, s in [k.split("|")] if s in ("same", "rand")}  # fmt: skip
    out["agreement_with_d3v4_swap_main"] = swap_agreement(rows)
    return out


def swap_agreement(rows: list[dict]) -> dict | None:
    """The answer roles of the dissoc rows against pointer_swap's d3v4_swap_main (same scenes, same edits): share of
    (item, group, layer) matched with the same role (bf16 batch rounding may flip near ties)."""
    path = pins.RESULTS_DIR / "pointer_swap" / "d3v4_swap_main" / "outcomes.jsonl"
    if not path.exists():
        return None
    theirs = {}
    for line in path.read_text().splitlines():
        o = json.loads(line)
        if o["source"] == "dissoc":
            theirs[(o["name"], o["group"], o["layer"])] = o["role"]
    pairs = [(r["role"], theirs[(r["id"], r["group"], r["layer"])]) for r in rows
             if r["source"] == "dissoc" and (r["id"], r["group"], r["layer"]) in theirs]  # fmt: skip
    return {"n": len(pairs), "same_role": statistics.mean(a == b for a, b in pairs) if pairs else None}


def load_run(name: str) -> tuple[dict, list[dict]]:
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    return m, [json.loads(x) for x in (out_dir / "rows.jsonl").read_text().splitlines()]


def _ci(s: dict | None) -> str:
    if not s or not s.get("n"):
        return "-"
    return (
        f"{100 * s['share']:.0f}% [{100 * s['cluster'][0]:.0f}, {100 * s['cluster'][1]:.0f}] (Wilson "
        f"[{100 * s['wilson'][0]:.0f}, {100 * s['wilson'][1]:.0f}]; n={s['n']} / k={s['k']} / t={s['t']})"
    )


def reader_name(rd: str) -> str:
    return "the J-lens" if rd == "lens" else f"layer {rd.split(':')[0]}, head {rd.split(':')[1]}"


def stage_summarise(name: str) -> None:
    m, rows = load_run(name)
    a = analyse(m, rows)
    out_dir = RESULTS / name / f"analysis-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out_dir.mkdir(parents=True, exist_ok=False)
    (out_dir / "summary.json").write_text(json.dumps(a, indent=2) + "\n")
    lines = [f"# {EXP} / {name}", "", f"Primary ({reader_name(m['heads'][0])}, memory → prompt, dissoc): "
             f"{a['primary']['verdict']}", ""]  # fmt: skip
    for fam, cells in a["cells"].items():
        for rd, sc in cells.items():
            if rd == "paired_vs_lens":
                continue
            lines.append(f"- {FAMILY_WORDS.get(fam, fam)}, {reader_name(rd)}: moved -> new statement {_ci(sc['moved_new'])}; "
                         f"moved -> org statement {_ci(sc['moved_org'])}; kept -> org statement {_ci(sc['kept_org'])}")  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:6]))


# ---- figures and report ----------------------------------------------------------------------------------------------


def fig_readers(a: dict, m: dict, stem: Path) -> list[str]:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import MUTED, percent_axis, style_axes
    from scripts.attn_knockout import _save  # the D2 caption layout (rows; the figure grows with its caption)

    readers = [*m["heads"], *(["lens"] if m["lens"] else [])]
    fams = [f for f in ("RL", "DL", "RR") if f in a["cells"]]
    fig, axes = plt.subplots(1, len(fams), figsize=(4.8 * len(fams), 3.6), squeeze=False, sharey=True)
    series = (("moved_new", "#2a78d6", "o", "answer moved: looks most at the statement of the new answer"),
              ("moved_org", "#eb6834", "s", "answer moved: looks most at the org prompt's asked statement"),
              ("kept_org", "#1baf7a", "^", "answer kept: looks most at the asked statement"))  # fmt: skip
    for j, f in enumerate(fams):
        ax = axes[0][j]
        style_axes(ax)
        for k, (key, color, marker, _) in enumerate(series):
            xs, ys, lo, hi = [], [], [], []
            for i, rd in enumerate(readers):
                s = a["cells"][f][rd][key]
                if s.get("n"):
                    xs.append(i + (k - 1) * 0.22)
                    ys.append(s["share"])
                    lo.append(max(0.0, s["share"] - s["cluster"][0]))
                    hi.append(max(0.0, s["cluster"][1] - s["share"]))
            ax.errorbar(xs, ys, yerr=[lo, hi], fmt=marker, color=color, ms=5, lw=1, capsize=0, mec="#fcfcfb")
        if f == "RL":
            ax.axhline(FOLLOW_MOVED, color=MUTED, lw=0.6, ls=":")
            ax.axhline(FOLLOW_STAY, color=MUTED, lw=0.6, ls="--")
        ax.set_xticks(range(len(readers)), ["J-lens\n(word)" if rd == "lens" else f"L{rd.split(':')[0]}\nhead {rd.split(':')[1]}"
                                            for rd in readers], fontsize=7)  # fmt: skip
        ax.set_ylim(-0.04, 1.06)
        percent_axis(ax)
        n = a["cells"][f][readers[0]]["moved_new"].get("n", 0)
        ax.set_title(f"{FAMILY_WORDS.get(f, f)} ({n} moved rows)", fontsize=8.5, loc="left")
        if j == 0:
            ax.set_ylabel("% of rows", fontsize=8, color=MUTED)
    handles = [Line2D([], [], color=c, marker=mk, ls="none", ms=6, label=lab) for _, c, mk, lab in series]
    handles += [Line2D([], [], color=MUTED, lw=0.6, ls=":", label=f"bar for moved rows ({FOLLOW_MOVED:.0%})"),
                Line2D([], [], color=MUTED, lw=0.6, ls="--", label=f"bar for kept rows ({FOLLOW_STAY:.0%})")]  # fmt: skip
    ex = EXAMPLE.get("text", "")
    pl = EXAMPLE.get("patch_layers", "48 or 50")
    explain = [
        ("What we did", f"Replaced the org prompt's last tokens (or the tokens after the question) at layer {pl} "
                        "with the alt prompt's (bridge alt at another statement), then asked which statement each "
                        "late head looks at most from the last token, and which entity the J-lens reads there."),
        ("Example", ex),
        ("How to read", "Blue: rows whose answer moved to another statement; high = the head follows the pointer. "
                        "Orange: the same rows, the head still on the org statement (it ignores the pointer). Green: "
                        "rows whose answer stayed, the head on the org statement."),
        ("Control", "Memory → memory has no lookup: there the answer comes from memory, and 'new statement' is the "
                    "alt entity's (where the bridge moved). The same-entity patch and a random push are in the report."),
    ]  # fmt: skip
    data = (f"{m['model']['repo'].split('/')[-1]}; pointer_v4 scenes (countries, animals, body parts), the four patch "
            "settings pooled; error bars: entity-cluster bootstrap 95% CI (entities resampled within topic).")  # fmt: skip
    return _save(fig, stem, "After a patch moves the answer, does the late head look at the new statement?", explain,
                 data, handles, 3)  # fmt: skip


EXAMPLE: dict[str, str] = {}


def stage_figures(name: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    m, rows = load_run(name)
    a = analyse(m, rows)
    ex_path = RESULTS / name / "examples.json"
    EXAMPLE.clear()
    pls = json.loads((RESULTS / name / "check.json").read_text())["patch_layers"]
    EXAMPLE["patch_layers"] = " or ".join(map(str, pls))
    if ex_path.exists():
        exs = json.loads(ex_path.read_text())["examples"]
        pick = next((e for e in exs if e["group"] == "head_follows"), exs[0] if exs else None)
        if pick:
            EXAMPLE["text"] = pick["why_short"]
    final_dir = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}-figures"
    out_dir = final_dir.with_name(final_dir.name + ".partial")
    for old in (RESULTS / name).glob("analysis-*-figures*"):  # one figures folder per run
        if old.is_dir():
            shutil.rmtree(old)
    out_dir.mkdir(parents=True, exist_ok=False)
    figs = {"readers": fig_readers(a, m, out_dir / "readers")}
    (out_dir / "summary.json").write_text(json.dumps({"run": name, "analysis": a, "figures": figs}, indent=2) + "\n")
    (out_dir / "report.md").write_text(report_md(name, m, rows, a, figs))
    out_dir.rename(final_dir)
    print("wrote", final_dir, figs)


def _spec(name: str) -> dict:
    import yaml

    path = pins.REPO_ROOT / "jobs" / "d5" / f"{name}.yaml"
    return yaml.safe_load(path.read_text()) if path.exists() else {}


def report_md(name: str, m: dict, rows: list[dict], a: dict, figs: dict) -> str:
    spec = _spec(name)
    head = m["heads"][0]
    check = json.loads((RESULTS / name / "check.json").read_text())
    prim = a["cells"].get("RL", {}).get(head, {})
    pl = a["cells"].get("RL", {}).get("paired_vs_lens", {})
    lens = a["cells"].get("RL", {}).get("lens", {})
    ctl = a["controls"]
    items = collections.Counter(r["family"] for r in rows if r["source"] == "unedited")
    lines = [f"# {EXP} / {name}: analysis", "",
             f"EXP {name} | model {m['model']['repo'].split('/')[-1]} | n={dict(items)} org prompts per family "
             f"(rows: 4 patch settings each) | seeds={sorted(set(m['seeds'].values()))}", "",
             f"Claim tested: {spec.get('question', m['why'])}", "",
             f"Headline: memory → prompt, {reader_name(head)}, rows whose answer moved to another statement: looks most "
             f"at the new answer's statement {_ci(prim.get('moved_new'))}; still at the asked statement "
             f"{_ci(prim.get('moved_org'))}   Baseline: rows whose answer stayed, on the asked statement "
             f"{_ci(prim.get('kept_org'))}   Control: the J-lens's word read on the same moved rows {_ci(lens.get('moved_new'))}"
             + (f"; head - lens {100 * pl['diff']:+.0f} points [{100 * pl['cluster'][0]:+.0f}, "
                f"{100 * pl['cluster'][1]:+.0f}] (entity cluster)" if pl.get("n") else ""),
             f"Verdict (pre-registered): {a['primary']['verdict']}", "",
             "Controls: " + "; ".join(f"{FAMILY_WORDS.get(k.split('|')[0], k)}, {k.split('|')[1]}: answer changed "
                                      f"{_ci(v['moved'])}, head on the asked statement {_ci(v['head_org'])}"
                                      for k, v in ctl.items() if k.split("|")[1] in ("same", "rand")),
             "",
             "Figures: " + ", ".join(f for fs in figs.values() if fs for f in fs), "",
             "Three dumbest ways this could be wrong:",
             "1) The head looks at the new statement because the patch copied the alt prompt's whole last-token state, "
             "including its attention query, so 'follows' only says the query moved with the patch. Checked: that is "
             "the question here (does the query carry the pointer); the same-entity patch copies a state too and "
             f"must leave the head on the asked statement ({_ci(ctl.get('RL|same', {}).get('head_org'))}).",
             f"2) Statement spans or the role map are off. Checked: the answer roles agree with d3v4_swap_main on the "
             f"same items and edits in {_agree(a)}; every statement has tokens (asserted); a self-patch changes the "
             f"logits by at most {check['self_patch_max_abs']:.3f}.",
             "3) Few entities carry the result. Checked: every interval is the entity-cluster bootstrap (k entities "
             "next to every number); per topic in the tables.",
             "",
             f"For the human to verify: rows.jsonl, family=RL, source=dissoc, outcome in {list(MOVED)}: count "
             f"heads['{head}']['top'] == new_statement (expect {round(prim.get('moved_new', {}).get('share', 0) * prim.get('moved_new', {}).get('n', 0))}/"
             f"{prim.get('moved_new', {}).get('n', 0)}).",
             "", "Status: UNVERIFIED", "", "## Pre-registered rule", "", "> " + m["decision"].replace("\n", " "), "",
             "## Every reader and family (dissoc, settings pooled)", "",
             "| family | reader | moved: new statement | moved: asked statement | kept: asked statement |", "|---|---|---|---|---|"]  # fmt: skip
    for fam, cells in a["cells"].items():
        for rd, sc in cells.items():
            if rd != "paired_vs_lens":
                lines.append(f"| {FAMILY_WORDS.get(fam, fam)} | {reader_name(rd)} | {_ci(sc['moved_new'])} | "
                             f"{_ci(sc['moved_org'])} | {_ci(sc['kept_org'])} |")  # fmt: skip
    lines += ["", "## By patch setting (layer 51 head 22)", "", "| family | patched tokens | layer | answer moved | "
              "moved: new statement | kept: asked statement |", "|---|---|---|---|---|---|"]  # fmt: skip
    for k, v in a["settings"].items():
        fam, grp, la = k.split("|")
        lines.append(f"| {FAMILY_WORDS.get(fam, fam)} | {'the last two tokens' if grp == 'last' else 'every token after the question'} | "
                     f"{la} | {_ci(v['moved'])} | {_ci(v['head']['moved_new'])} | {_ci(v['head']['kept_org'])} |")  # fmt: skip
    lines += ["", "## By outcome (dissoc): share naming the new answer's statement", "",
              "| family | outcome | " + " | ".join(reader_name(rd) for rd in [*m["heads"], *(["lens"] if m["lens"] else [])]) + " |",
              "|---|---|" + "---|" * (len(m["heads"]) + (1 if m["lens"] else 0))]  # fmt: skip
    for k, v in a["outcomes"].items():
        if "|" in k:
            fam, kind = k.split("|")
            lines.append(f"| {FAMILY_WORDS.get(fam, fam)} | {kind} | " + " | ".join(_ci(s) for s in v.values()) + " |")
    lines += ["", "## Per topic (layer 51 head 22, memory → prompt, moved rows: new statement)", ""]
    pt = prim.get("moved_new", {}).get("per_topic", {})
    lines += [f"- {d}: {100 * v['share']:.0f}% (n={v['n']})" for d, v in pt.items()]
    lines += ["", "## The agent's priors (job spec hypotheses), checked", "", "| hypothesis | prediction | result | verdict |",
              "|---|---|---|---|"]  # fmt: skip
    for h, pred in (spec.get("hypotheses") or {}).items():
        res, ver = prior_check(h, a, m)
        lines.append(f"| {h} | {pred if len(pred) <= 200 else pred[:197] + '...'} | {res} | {ver} |")
    return "\n".join(lines) + "\n"


def _agree(a: dict) -> str:
    g = a.get("agreement_with_d3v4_swap_main")
    return f"{100 * g['same_role']:.1f}% of {g['n']} (item, tokens, layer)" if g and g.get("n") else "- (no overlap)"


def prior_check(h: str, a: dict, m: dict) -> tuple[str, str]:
    head = m["heads"][0]
    prim = a["cells"].get("RL", {}).get(head)
    if not prim:
        return "not measured", "-"
    if h == "H_head_follows":
        return (f"moved -> new {_ci(prim['moved_new'])}; kept -> asked {_ci(prim['kept_org'])}",
                {True: "holds", False: "fails", None: "-"}[a["primary"].get("follows")])  # fmt: skip
    if h == "H_head_static":
        return f"moved -> asked {_ci(prim['moved_org'])}", {True: "holds", False: "fails", None: "-"}[a["primary"].get("static")]  # fmt: skip
    if h == "H_head_beats_lens":
        pl = a["cells"]["RL"].get("paired_vs_lens", {})
        return ((f"head - lens {100 * pl['diff']:+.0f} [{100 * pl['cluster'][0]:+.0f}, {100 * pl['cluster'][1]:+.0f}]",
                 "holds" if pl["head_better"] else "fails") if pl.get("n") else ("no lens rows", "-"))  # fmt: skip
    if h == "H_controls":
        ok = a["controls_ok"]
        return ", ".join(f"{k}: {'ok' if v else 'moved > 10%'}" for k, v in ok.items()), "holds" if all(
            ok.values()
        ) else "fails"
    return "see summary.json", "-"


# ---- examples ------------------------------------------------------------------------------------------------------


def stage_examples(name: str, k: int) -> None:
    m, rows = load_run(name)
    path = RESULTS / name / "examples.json"
    assert not path.exists(), f"{path} exists; examples are written once"
    pm = run_manifest_items(m)
    items = {it["id"]: it for its in PS.load_items(pm).values() for it in its}
    tok = S.tokenizer()
    head = m["heads"][0]
    dis = [r for r in rows if r["source"] == "dissoc" and r["outcome"] in MOVED and r["new_statement"] is not None]
    groups = {
        "head_follows": ("The answer moved; the head looks at the new statement",
                         f"source dissoc, answer moved to another statement, {reader_name(head)} looks most at it",
                         [r for r in dis if reader_top(r, head) == r["new_statement"]]),
        "head_stays": ("The answer moved; the head stays on the asked statement",
                       f"as above, {reader_name(head)} still looks most at the org prompt's asked statement",
                       [r for r in dis if reader_top(r, head) == r["org_statement"]]),
        "lens_follows": ("The J-lens names the new answer's entity, the head does not", "moved rows, lens right, head not",
                         [r for r in dis if r.get("lens") and reader_top(r, "lens") == r["new_statement"]
                          and reader_top(r, head) != r["new_statement"]]),
        "same_control": ("Same-entity patch (control)", "source same: nothing should move",
                         [r for r in rows if r["source"] == "same"]),
    }  # fmt: skip
    rng = random.Random(EXAMPLE_SEED)
    examples = []
    for key, (_, why, pool) in groups.items():
        for r in rng.sample(pool, min(k, len(pool))):
            it = items[r["id"]]
            prep = PS.prepare(it, tok)
            text = prep["text"]
            spans, start = [], 0
            for i, stmt in enumerate(it["statements"]):
                a = text.index(stmt, start)
                start = a + len(stmt)
                roles = [x for x, j in (("asked statement", r["org_statement"]), ("new answer's statement", r["new_statement"]),
                                        ("head looks here most", reader_top(r, head))) if j == i]  # fmt: skip
                if roles:
                    spans.append({"start": a, "end": a + len(stmt), "role": roles[-1]})
            alt = it["sources"]["dissoc"]
            cond = (f"{'the last two tokens' if r['group'] == 'last' else 'every token after the question'} replaced at "
                    f"layer {r['layer']} by the alt prompt's ({r['source']}; alt question: {alt['question']!r})")  # fmt: skip
            short = (f"'... {it['statements'][r['org_statement']]} ... {it['question']}' -> answer org {it['answer']}; "
                     f"after the patch the answer is {r['top'].strip()!r} ({r['outcome']}), and {reader_name(head)} looks "
                     f"most at '{it['statements'][reader_top(r, head)]}'.")  # fmt: skip
            examples.append({"group": key, "family": r["family"], "item_id": r["id"], "prompt": text, "spans": spans,
                             "condition": cond, "why_short": short,
                             "answers": {"clean": it["answer"], "edited": r["top"].strip(),
                                         "expected": {"H_head_follows": f"head on statement {r['new_statement']}",
                                                      "H_head_static": f"head on statement {r['org_statement']}"}},
                             "numbers": {"role": r["role"], "outcome": r["outcome"], "head_masses": r["heads"][head]["masses"],
                                         "lens_top": reader_top(r, "lens")}, "why": why})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": EXAMPLE_SEED, "k": k,
            "groups": [{"key": g, "title": t, "definition": d, "n_total": len(p)} for g, (t, d, p) in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, {g["key"]: g["n_total"] for g in blob["groups"]})


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "examples", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--n", type=int, default=150, help="scenes per topic (pointer_swap's sample)")
    ap.add_argument("--families", nargs="+", default=["RL", "DL", "RR"])
    ap.add_argument("--domains", nargs="+", default=None)
    ap.add_argument("--heads", nargs="+", default=list(HEADS), help="layer:head, the first is the pre-registered one")
    ap.add_argument("--no-lens", action="store_true")
    ap.add_argument("--competence", default=None)
    ap.add_argument("--no-eligibility", action="store_true")
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "manifest":
        assert args.why, "manifest needs --why"
        stage_manifest(args)
    elif args.stage == "run":
        stage_run(args.name)
    elif args.stage == "summarise":
        stage_summarise(args.name)
    elif args.stage == "examples":
        stage_examples(args.name, args.k)
    else:
        stage_figures(args.name)
