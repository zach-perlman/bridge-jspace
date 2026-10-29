"""review_jspace: the review dashboard's "Look into J-space" panel (Dan 29 Oct 11:45, jobs/c3/batch53.yaml
inspector_1145 items 2-4). CPU only, read-only on results/; it writes only under review/ (notes in review/marks.jsonl)
and cache/ (readouts it keeps). Mounted by scripts/review.py (`make review-serve`): /jspace?view=..&item=.. per item.

Inputs: the states job's files (scripts/review_states.py): cache/review_states/<model>/<view>/<item>.npz (O / S states
at every layer at the item's tokens; the change's 25 signed-OMP atoms and X0's random part per layer), head.safetensors
(lm_head and final norm as loaded), and its run dir results/review_states/<run>/ (rank_check.jsonl, calib.jsonl). Where
the states job's head is missing, the pinned checkpoint's (x52_atoms fetch: cache/x52_atoms/<model>/head.safetensors).
The lens: the pinned J++ file (pins.TARGETS[model]["lenses"]["jpp"], its sha256 checked once).

The readout is Model.unembed and JLens.readout's arithmetic on the CPU: the J++ lens h -> h @ J_l^T, then the final
norm of the model's own kind on the bf16 input (Qwen: fp32 RMS x (1 + w); Muse: fp32 RMS by pow(-0.5) x w; NemotronH:
w x the bf16 RMS-normed input), lm_head in fp32 on the bf16 values, the logits rounded to bf16 as the GPU's bf16 matmul
returns them, then Muse's multiplier and softcap. A rank is 1 + the tokens with a strictly larger logit (x51_answer.
rank_of). Vectors at a token and layer: the state (O or S), the change S - O, its J++ part (the stored 25 atoms: their
unit lens vectors (g W_U[t]) J_l x the stored coefficients, X0's fit), the rest (change - J++ part), X0's random part of
the J++ part's share (stored), and the address part U (the routes test's pointer directions, at L only).

uv run python scripts/review_jspace.py rank-check            # item 3: docs/verify_pack_jspace.md + its verify_pack section
uv run python scripts/review_jspace.py selfcheck              # 51.12's answer-word ranks and x52_atoms' atoms, sample items
uv run python scripts/review_jspace.py rank-check --from-jread  # item 3 on the conflict test from 51.10's cached states
"""

from __future__ import annotations

import argparse
import collections
import functools
import gc
import html
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.review import items as I

E = html.escape
REPO = I.REPO  # where the panel may write (review/, cache/)
HEADS = I.REPO / "cache" / "x52_atoms"  # x52_atoms fetch's heads (read only)
STATES = REPO / "cache" / "review_states"
PANEL_CACHE = REPO / "cache" / "review_jspace"
MARKS = REPO / "review" / "marks.jsonl"
WRITE_ROOTS = ("review", "cache")
TOP = 30
TOP50 = 50
VECTORS = ("state", "change", "jpp", "rest", "rand", "U")
VECTOR_TEXT = {"state": "the state", "change": "the change (S minus O)", "jpp": "its J++ part (25 signed-OMP atoms)",
               "rest": "the rest (change minus J++ part)", "rand": "a random part of the J++ part's share",
               "U": "the address part (U, the pointer directions; at L only)"}  # fmt: skip
NORM_DEFAULT = {"qwen3.5-9b": "one_plus_weight_fp32", "qwen3.6-27b": "one_plus_weight_fp32",
                "qwen3.5-122b-a10b": "one_plus_weight_fp32", "muse-glimmer-30b": "weight_fp32_pow",
                "nemotron-3.5-lightning": "weight_after_cast"}  # fmt: skip


# ---- writes (review/ and cache/ only) ------------------------------------------------------------------------------


def guarded(path: Path) -> Path:
    """The path, if it lies under the repo's review/ or cache/ (cache/ may be a symlink); else AssertionError."""
    p = Path(path).resolve()
    roots = [(REPO / r).resolve() for r in WRITE_ROOTS]
    assert any(p == r or r in p.parents for r in roots), f"the J-space panel writes only under review/ and cache/: {p}"
    return Path(path)


def write_text(path: Path, text: str) -> None:
    p = guarded(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def append_line(path: Path, row: dict) -> None:
    p = guarded(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---- the model's readout on the CPU --------------------------------------------------------------------------------


def main_checkout() -> Path:
    """The main checkout (a worktree's results/ lacks the gitignored state files)."""
    out = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=REPO, capture_output=True, text=True).stdout
    return Path(out.strip()).resolve().parent if out.strip() else REPO


def config(model: str) -> dict:
    from huggingface_hub import hf_hub_download

    t = pins.TARGETS[model]
    c = json.loads(
        Path(hf_hub_download(t["repo"], "config.json", revision=t["revision"], local_files_only=True)).read_text()
    )
    return c.get("text_config", c.get("llm_config", c))


def head_path(model: str) -> tuple[Path, dict]:
    """The head file and its record: the states job's (as loaded on the GPU), else x52_atoms fetch's (the checkpoint's)."""
    p = STATES / model / "head.safetensors"
    if p.exists():
        return p, json.loads((STATES / model / "head.json").read_text())
    q = HEADS / model / "head.safetensors"
    if q.exists():
        c = config(model)
        return q, {"norm_kind": NORM_DEFAULT[model], "eps": c.get("rms_norm_eps", c.get("layer_norm_epsilon", 1e-6)),
                   "output_multiplier": c.get("output_multiplier"),
                   "final_logit_softcapping": c.get("final_logit_softcapping"), "source": "x52_atoms fetch"}  # fmt: skip
    raise FileNotFoundError(
        f"{model}: no head (cache/review_states/{model}/head.safetensors or cache/x52_atoms/{model}/)"
    )


def lens_file(model: str) -> Path:
    """The pinned J++ lens file, its sha256 checked once per (path, size, mtime) (marker under cache/review_jspace/)."""
    t = pins.TARGETS[model]
    src = t["lenses"]["jpp"]
    if src[0] == "local":
        path = I.REPO / src[1]
    else:
        from huggingface_hub import hf_hub_download

        path = Path(hf_hub_download(src[0], src[1], revision=src[2], local_files_only=True))
    want = t.get("frozen_lens_sha256", pins.FROZEN_LENS_SHA256)
    st = path.stat()
    key = {"path": str(path.resolve()), "size": st.st_size, "mtime": st.st_mtime, "sha256": want}
    marker = PANEL_CACHE / "lens_checked" / f"{model}.json"
    if not (marker.exists() and json.loads(marker.read_text()) == key):
        assert pins.sha256_file(path) == want, f"{path} is not {model}'s pinned J++ lens"
        write_text(marker, json.dumps(key) + "\n")
    return path


class Readout:
    """One model's readout on the CPU: W_U (fp32), the final norm, the lens maps (fp32 per layer, a few kept)."""

    def __init__(self, model: str):
        import torch
        from safetensors.torch import load_file

        from scripts import review_states as RS

        self.model = model
        path, self.head = head_path(model)
        t = load_file(str(path))
        self.w_u = t["lm_head.weight"].float()
        self.norm_w = t["norm.weight"]
        self.kind = self.head.get("norm_kind") or NORM_DEFAULT[model]
        self.eps = float(self.head.get("eps") or 1e-6)
        self.mult = self.head.get("output_multiplier")
        self.cap = self.head.get("final_logit_softcapping")
        gain = pins.TARGETS[model]["norm_gain"]
        self.gain = (1.0 + self.norm_w.float()) if gain == "one_plus_weight" else self.norm_w.float()
        self.blob = torch.load(lens_file(model), map_location="cpu", weights_only=True, mmap=True)
        self.lens_layers = [int(x) for x in self.blob["source_layers"]]
        self.tok = RS.hf_tokenizer(model)
        self._J: collections.OrderedDict = collections.OrderedDict()

    def J(self, layer: int):
        if layer not in self._J:
            self._J[layer] = self.blob["J"][layer].float()
            while len(self._J) > 4:
                self._J.popitem(last=False)
        return self._J[layer]

    def norm(self, x):
        import torch

        xb = x.to(torch.bfloat16)
        x32 = xb.float()
        var = x32.pow(2).mean(-1, keepdim=True)
        if self.kind == "one_plus_weight_fp32":
            return (x32 * torch.rsqrt(var + self.eps) * (1.0 + self.norm_w.float())).to(torch.bfloat16)
        if self.kind == "weight_fp32_pow":
            return (x32 * torch.pow(var + self.eps, -0.5) * self.norm_w.float()).to(torch.bfloat16)
        if self.kind == "weight_after_cast":
            return self.norm_w.to(torch.bfloat16) * (x32 * torch.rsqrt(var + self.eps)).to(torch.bfloat16)
        raise ValueError(f"{self.model}: unknown final norm {self.kind!r}")

    def unembed(self, x):
        """Model.unembed on the CPU: [n, d] -> [n, vocab] fp32 logits (bf16-rounded as the GPU returns them)."""
        import torch

        logits = (self.norm(x).float() @ self.w_u.T).to(torch.bfloat16).float()
        if self.mult:
            logits = logits * float(self.mult)
        if self.cap:
            logits = float(self.cap) * torch.tanh(logits / float(self.cap))
        return logits

    def lens(self, h, layer: int):
        """JLens.readout on the CPU: unembed(h @ J_l^T)."""
        return self.unembed(h.float() @ self.J(layer).T)

    def atom_rows(self, layer: int, ids) -> Any:
        """X0's dictionary rows for these tokens: unit (g W_U[t]) J_l (JLens.vectors)."""
        import torch

        rows = (self.w_u[torch.as_tensor(ids, dtype=torch.long)] * self.gain) @ self.J(layer)
        return torch.nn.functional.normalize(rows, dim=-1)

    def decode(self, t: int) -> str:
        return str(self.tok.decode([int(t)]))


_LOADED: dict[str, Readout] = {}


def readout(model: str) -> Readout:
    """One model at a time (the previous one is dropped: W_U and the lens maps are GBs)."""
    if model not in _LOADED:
        _LOADED.clear()
        gc.collect()
        _LOADED[model] = Readout(model)
    return _LOADED[model]


def rank_of(logits, ids) -> tuple[int | None, int | None]:
    """The best rank (1 = top; strictly larger logits counted) among ids, and the id that has it."""
    best = None
    for t in ids:
        r = int((logits > logits[int(t)]).sum()) + 1
        if best is None or r < best[0]:
            best = (r, int(t))
    return best if best else (None, None)


# ---- the item's states and vectors ---------------------------------------------------------------------------------


@functools.lru_cache(maxsize=8)
def states(model: str, view_id: str, item_id: str) -> dict | None:
    from scripts import review_states as RS

    p = STATES / model / RS.item_file(view_id, item_id)
    if not p.exists():
        return None
    z = np.load(p)
    out = {k: z[k] for k in z.files if k != "meta"}
    out["meta"] = json.loads(str(z["meta"]))
    return out


@functools.lru_cache(maxsize=8)
def pointer_u(model: str):
    """The routes test's pointer directions U at L (review_states.pointer_basis on the model's routes run)."""
    import torch

    from scripts import review_states as RS

    runs = I.view("routes")["runs"].get(model, [])
    if not runs:
        return None
    old = pins.TARGET
    try:  # pointer_basis reads x6_routes.STATES[pins.TARGET] when the run's manifest names none
        pins.TARGET = model
        return torch.tensor(np.asarray(RS.pointer_basis(runs[0])), dtype=torch.float32)
    finally:
        pins.TARGET = old


def model_layer(model: str) -> int:
    return int(I.spec()["models"][model]["layer"])


def vector(st: dict, model: str, prompt: str, pos: int, layer: int, kind: str):
    """The chosen vector [d] (fp32), or (None, why)."""
    import torch

    po, ps = [int(x) for x in st["pos_O"]], [int(x) for x in st["pos_S"]]
    if kind == "state":
        arr, pl = (st["h_O"], po) if prompt == "O" else (st["h_S"], ps)
        if pos not in pl:
            return None, f"position {pos} is not saved in {prompt}"
        return torch.tensor(arr[pl.index(pos), layer].astype(np.float32)), ""
    pairs = [tuple(int(v) for v in p) for p in st["pairs"]]
    r = next((i for i, (a, _) in enumerate(pairs) if po[a] == pos), None)
    if r is None:
        return None, f"no change at position {pos} (O and S do not align there)"
    a, b = pairs[r]
    x = torch.tensor(st["h_S"][b, layer].astype(np.float32) - st["h_O"][a, layer].astype(np.float32))
    if kind == "change":
        return x, ""
    if kind == "rand":
        return torch.tensor(st["rand"][r, layer].astype(np.float32)), ""
    if kind in ("jpp", "rest"):
        ids = st["atoms_ids"][r, layer]
        if (ids < 0).any():
            return None, f"no J++ map at layer {layer}"
        part = torch.tensor(st["atoms_coef"][r, layer].astype(np.float32)) @ readout(model).atom_rows(
            layer, ids.tolist()
        )
        return (part if kind == "jpp" else x - part), ""
    if kind == "U":
        if layer != model_layer(model):
            return None, f"U is fit at L{model_layer(model)} only"
        u = pointer_u(model)
        if u is None:
            return None, "no routes run (no pointer directions) for this model"
        return (x @ u) @ u.T, ""
    raise ValueError(kind)


# ---- the tokens always listed --------------------------------------------------------------------------------------

LOCKER = re.compile(r"[Tt]he locker of (?:the )?([\w-]+) is")
PICKED = re.compile(r"\b[A-Z][a-z]+ picked (?:the )?([\w-]+)\.")


def scene_items(case: dict) -> list[str]:
    texts = [case.get("context", ""), case.get("cf_context", "")]
    names = {m.group(1) for t in texts for m in LOCKER.finditer(t)} | {
        m.group(1) for t in texts for m in PICKED.finditer(t)
    }
    return sorted(names - {case.get("bridge"), case.get("cf_bridge")})


def listed_tokens(it: dict, tok) -> list[tuple[str, list[int]]]:
    """(label, token ids) always listed: both bridge words (spellings, symbol; first pieces apart), every item of the
    scene, both readers' O and S answers (digit; number word; a word answer's first tokens)."""
    from scripts import review_states as RS
    from scripts import x51_answer as A

    case = it["case"] or {}
    dom = case.get("domain")
    out = []
    for who, name in (("O's bridge", case.get("bridge")), ("S's bridge", case.get("cf_bridge"))):
        if name:
            v = RS.variant_tokens(tok, name, dom)
            out += [(f"{who}: {name}", v["word"]), (f"{who}: {name} (with first pieces)", v["pieces"])]
    for name in scene_items(case):
        out.append((f"scene item: {name}", RS.variant_tokens(tok, name, dom)["word"]))
    for w, rd in (case.get("readers") or {}).items():
        for which, key, tid in (("O", "answer", "tok_A"), ("S", "cf_answer", "tok_b")):
            a = str(rd.get(key, ""))
            if not a:
                continue
            reader = I.READER_NAME.get(w, w)
            if a.isdigit():
                t = RS.answer_tokens(tok, a, rd.get(tid))
                out += [(f"{reader}'s {which} answer {a} (digit)", t["digit"])]
                if t["word"]:
                    out += [(f"{reader}'s {which} answer {a} (word)", t["word"])]
            else:
                out += [(f"{reader}'s {which} answer: {a}", A.variant_ids(tok, [a]))]
    return [(label, ids) for label, ids in out if ids]


def typed_tokens(text: str, tok) -> list[tuple[str, list[int], str]]:
    """One token per line, as typed (a leading space counts); '#123' is the id 123. A word of several tokens is read
    by its first token (said beside)."""
    out = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if re.fullmatch(r"#\d+", line.strip()):
            t = int(line.strip()[1:])
            out.append((line.strip(), [t], ""))
            continue
        ids = tok(line, add_special_tokens=False).input_ids
        if ids:
            note = "" if len(ids) == 1 else f"first of {len(ids)} tokens: {[str(tok.decode([i])) for i in ids]}"
            out.append((repr(line), [int(ids[0])], note))
    return out


# ---- atoms and their classes (x52_atoms' classifier) ---------------------------------------------------------------


def atom_context(it: dict, tok) -> dict | None:
    """x52_atoms' classifier context for an item in its reader's view (E1-style: number answers; word answers as Z2)."""
    from scripts import x52_atoms as AT

    case = it["case"]
    if not case:
        return None
    dom = case.get("domain")
    w = it["reader"]
    answers = {r: [str(rd.get("answer", "")), str(rd.get("cf_answer", ""))] for r, rd in case["readers"].items()}
    other = next((r for r in answers if r != w), None)

    def ans(xs: list[str]) -> dict:
        xs = [x for x in xs if x]
        return (
            AT.number_matcher(xs)
            if xs and all(x.isdigit() and len(x) == 1 for x in xs)
            else AT.word_answer_matcher(tok, xs)
        )

    items = scene_items(case)
    texts = [case.get("context", ""), case.get("cf_context", "")]
    persons = {m.group(1) for t in texts for m in AT.PICKED.finditer(t)}
    in_scene = {case.get("bridge"), case.get("cf_bridge"), *items}
    same = sorted(set(AT.SAME_CLASS.get(dom, [])) - in_scene) if dom else []
    return {"bridge": AT.entity_matcher(tok, [case["bridge"]], dom, spell=True),
            "new_bridge": AT.entity_matcher(tok, [case["cf_bridge"]], dom, spell=True),
            "scene_item": AT.entity_matcher(tok, items, dom), "person": AT.matcher(AT.word_keys_all(sorted(persons))),
            "answer_own": ans(answers[w]), "answer_other": ans(answers[other]) if other else AT.matcher(),
            "same_class": AT.entity_matcher(tok, same, dom) if same else AT.matcher(), "answer_kind": AT.NUMBER_KIND,
            "prompt_keys": AT.prompt_keys(" ".join(texts))}  # fmt: skip


DAN_CLASS = {"bridge": "bridge", "new_bridge": "new bridge", "answer_own": "answer", "answer_other": "answer"}


def atoms_at(st: dict, it: dict, model: str, pos: int, layer: int) -> list[dict]:
    """The change's 25 atoms at (pos, layer): token, signed coefficient, energy share, class (Dan's four; x52's beside)."""
    from scripts import x52_atoms as AT

    po = [int(x) for x in st["pos_O"]]
    pairs = [tuple(int(v) for v in p) for p in st["pairs"]]
    r = next((i for i, (a, _) in enumerate(pairs) if po[a] == pos), None)
    if r is None or (st["atoms_ids"][r, layer] < 0).any():
        return []
    ro = readout(model)
    ctx = atom_context(it, ro.tok)
    out = []
    for k, (t, c, g) in enumerate(zip(st["atoms_ids"][r, layer], st["atoms_coef"][r, layer], st["atoms_gain"][r, layer],
                                      strict=True)):  # fmt: skip
        text = ro.decode(int(t))
        cls = AT.classify(text, int(t), ctx)[0] if ctx else "other"
        out.append({"rank": k + 1, "token_id": int(t), "token": text, "coef": float(c), "share": float(g),
                    "class": DAN_CLASS.get(cls, "other"), "x52_class": cls})  # fmt: skip
    return out


# ---- self-checks: 51.12's stored answer-word rank, x52_atoms' atoms ------------------------------------------------


@functools.lru_cache(maxsize=16)
def x51_rows(model: str) -> tuple[dict, dict]:
    """51.12 E1's readout rows by (scene, variant) and its cases by scene (own-word tokens), for the model."""
    from scripts import x51_answer as A

    run = A.runs_of("e1").get(model)
    if not run:
        return {}, {}
    d = f"results/x51_answer/{run}"
    rd = {(r["key"], r["variant"]): r for r in I.read_jsonl(f"{d}/readout.jsonl") if r.get("source") == "PP"}
    cs = {c["key"]: c for c in I.read_jsonl(f"{d}/cases.jsonl")}
    return rd, cs


@functools.lru_cache(maxsize=16)
def x52_rows(model: str) -> dict[str, dict]:
    """x52_atoms' E1 atoms by scene (the lookup's Δ at L), from the model's forward or states run."""
    from scripts import x52_atoms as AT

    for run in (AT.FWD_RUNS.get(model), AT.STATES_RUNS.get(model)):
        rows = I.read_jsonl(f"results/x52_atoms/{run}/atoms.jsonl") if run else ()
        if rows:
            return {r["key"]: r for r in rows if r["set"] == "e1" and r["reader"] == "PP"}
    return {}


def check_51_12(st: dict, it: dict, model: str) -> list[dict]:
    """At L and the bridge word: the panel's own-answer-word rank on O and S vs 51.12's stored one (same item, reader)."""
    import torch

    rd, cs = x51_rows(model)
    c = cs.get(it["scene"])
    la = model_layer(model)
    if not c or not rd:
        return []
    ro = readout(model)
    out = []
    pos = int(st["meta"]["pos"])
    for v, prompt in (("org", "O"), ("alt", "S")):
        row = rd.get((it["scene"], v))
        ids = c["tokens"]["own_word"][v].get(it["reader"]) if row else None
        h, _ = vector(st, model, prompt, pos, la, "state")
        if row is None or not ids or h is None:
            continue
        lg = ro.lens(torch.as_tensor(h)[None], la)[0]
        mine = rank_of(lg, ids)[0]
        theirs = row["answer_word_rank"].get(it["reader"])
        # 51.12's states come from its own forward: equal, or bf16 noise between two runs' forwards (relative gap shown)
        gap = abs(mine - theirs) / max(mine, theirs) if mine and theirs else None
        out.append({"check": f"51.12 answer-word rank on {prompt}", "panel": mine, "stored": theirs, "ok": mine == theirs,
                    "rel_gap": gap})  # fmt: skip
    return out


def check_x52(st: dict, it: dict, model: str) -> list[dict]:
    """At L and the bridge word: the panel's 25 atoms (the states job's fit) vs x52_atoms' for the same scene."""
    row = x52_rows(model).get(it["scene"])
    if row is None or it["kind"] not in ("x0", "x51_answer"):
        return []
    atoms = atoms_at(st, it, model, int(st["meta"]["pos"]), model_layer(model))
    if not atoms:
        return []
    mine, theirs = [a["token_id"] for a in atoms], [a["token_id"] for a in row["atoms"]]
    gap = max(abs(a["coef"] - b["coef"]) for a, b in zip(atoms, row["atoms"], strict=True)) if mine == theirs else None
    return [{"check": "x52_atoms' 25 atoms (ids in order)", "panel": len(set(mine) & set(theirs)), "stored": len(theirs),
             "ok": mine == theirs, "max_coef_gap": gap}]  # fmt: skip


# ---- the page ------------------------------------------------------------------------------------------------------

CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e3e3e6;--ok:#2f7d4f;--bad:#b8433a;--hl:#fff1a8}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#e8e8ea;--mut:#9a9aa2;--card:#202024;--line:#36363c;--hl:#5a4b10}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,system-ui,sans-serif;margin:0;padding:16px}
main{max-width:1280px;margin:auto}.mut{color:var(--mut)}a{color:#2c6db5}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;margin:10px 0}
form.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:end}form.ctl label{display:flex;flex-direction:column;font-size:12px}
input,select,textarea,button{font:inherit}table{border-collapse:collapse}td,th{border-bottom:1px solid var(--line);padding:2px 6px;
text-align:left;font-size:12.5px;vertical-align:top}th{color:var(--mut);font-weight:500}.cols{display:flex;gap:16px;flex-wrap:wrap}
code,.tk{font-family:ui-monospace,Menlo,monospace;font-size:12px}.ok{color:var(--ok)}.bad{color:var(--bad);font-weight:600}
.heat td{text-align:center;min-width:26px;font-size:11px;padding:1px 2px}.wrap{overflow-x:auto}
"""


def tk(s: str) -> str:
    return "<span class='tk'>" + E(json.dumps(s, ensure_ascii=False)) + "</span>"


def find_item(view_id: str, item_id: str) -> dict:
    model = item_id.split("|", 1)[0]
    got = next((it for it in I.items(view_id, model) if it["id"] == item_id), None)
    if got is None:
        raise KeyError(f"{item_id} is not in {view_id}'s item set")
    return got


def jspace_notes(item_id: str) -> list[dict]:
    if not MARKS.exists():
        return []
    rows = [json.loads(line) for line in MARKS.read_text().splitlines() if line.strip()]
    return [r for r in rows if r.get("kind") == "jspace" and r.get("item") == item_id]


def heat_color(rank: int | None, n_vocab: int) -> str:
    if rank is None:
        return "transparent"
    s = 1 - math.log(rank) / math.log(n_vocab)  # 1 at the top, 0 at the bottom
    return f"hsla(140,55%,40%,{max(0.0, s) ** 3:.2f})"


def heatmap(st: dict, model: str, prompt: str, kind: str, lens_name: str, token: int) -> dict:
    """Rank of one token at every saved position x every layer for the chosen vector (kept under cache/review_jspace/)."""
    import torch

    key = f"{model}|{st['meta']['view']}|{st['meta']['item']}|{prompt}|{kind}|{lens_name}|{token}"
    f = PANEL_CACHE / "heat" / (re.sub(r"[^\w.-]+", "_", key)[:180] + ".json")
    if f.exists():
        return json.loads(f.read_text())
    ro = readout(model)
    positions = [int(x) for x in (st["pos_O"] if prompt == "O" or kind != "state" else st["pos_S"])]
    n_layers = st["h_O"].shape[1]
    layers = [la for la in range(n_layers) if lens_name == "logit" or la in ro.lens_layers]
    grid: dict[str, dict[str, int | None]] = {}
    t0 = time.time()
    xs, where = [], []
    for la in layers:  # each layer's vectors through its lens map, then one batched unembedding
        vecs, ok = [], []
        for p in positions:
            v, _ = vector(st, model, prompt, p, la, kind)
            if v is not None:
                vecs.append(v)
                ok.append(p)
        if vecs:
            x = torch.stack(vecs)
            xs.append(x @ ro.J(la).T if lens_name == "jpp" else x)
            where += [(p, la) for p in ok]
    if xs:
        x = torch.cat(xs)
        for s in range(0, x.shape[0], 512):
            lg = ro.unembed(x[s : s + 512])
            for (p, la), r in zip(
                where[s : s + 512], ((lg > lg[:, token : token + 1]).sum(1) + 1).tolist(), strict=True
            ):
                grid.setdefault(str(p), {})[str(la)] = int(r)
    out = {"positions": positions, "layers": layers, "grid": grid, "seconds": round(time.time() - t0, 1)}
    write_text(f, json.dumps(out))
    return out


def page(q: dict[str, str], server: bool = True) -> str:
    """The panel for one item: controls, the J++ and logit-lens top 30, typed and listed tokens' ranks, a token x layer
    heatmap, the change's 25 atoms at L, the self-checks and the note form."""
    import torch

    view_id, item_id = q["view"], q["item"]
    it = find_item(view_id, item_id)
    model = it["model"]
    st = states(model, view_id, item_id)
    head = (f"<h1>Look into J-space</h1><p><a href='/view?{urlencode({'view': view_id})}'>back to {E(view_id)}</a> · "
            f"<code>{E(item_id)}</code> · {E(I.spec()['models'][model]['label'])} · reader "
            f"{E(str(I.READER_NAME.get(it['reader'], it['reader'])))}</p>")  # fmt: skip
    if st is None:
        return doc(
            head + "<div class='box'>No states for this item yet: the states job (scripts/review_states.py, "
            f"x53_inspector_states_*) writes cache/review_states/{E(model)}/. Pull them from the box.</div>"
        )
    ro = readout(model)
    la_default = int(st["meta"].get("layer") or model_layer(model))
    pos_default = int(st["meta"]["pos"])
    prompt = q.get("prompt") or "O"
    pos = int(q.get("pos") or pos_default)
    layer = int(q.get("layer") or la_default)
    kind = q.get("vector") or "state"
    typed = q.get("tokens") or ""
    n_layers = st["h_O"].shape[1]
    roles = st["meta"]["roles_O" if prompt == "O" else "roles_S"]
    ids = st["ids_O"] if prompt == "O" else st["ids_S"]
    opts = "".join(f"<option value='{p}'{' selected' if int(p) == pos else ''}>{p}: {E(ro.decode(int(ids[int(p)])))} "
                   f"({E(', '.join(r))})</option>" for p, r in roles.items())  # fmt: skip
    sel = lambda name, vals, cur: "".join(  # noqa: E731
        f"<option value='{E(str(v))}'{' selected' if str(v) == str(cur) else ''}>{E(str(t))}</option>" for v, t in vals
    )
    form = (f"<form class='ctl box' method='get' action='/jspace'><input type='hidden' name='view' value='{E(view_id)}'>"
            f"<input type='hidden' name='item' value='{E(item_id)}'>"
            f"<label>prompt<select name='prompt'>{sel('prompt', [('O', 'O (original)'), ('S', 'S (changed)')], prompt)}</select></label>"
            f"<label>token<select name='pos'>{opts}</select></label>"
            f"<label>layer<select name='layer'>{sel('layer', [(x, f'L{x}') for x in range(n_layers)], layer)}</select></label>"
            f"<label>vector<select name='vector'>{sel('vector', [(v, VECTOR_TEXT[v]) for v in VECTORS], kind)}</select></label>"
            f"<label>tokens (one per line, as typed; #id for an id)<textarea name='tokens' rows='3' cols='28'>{E(typed)}</textarea></label>"
            f"<label>heatmap token<input name='heat' value='{E(q.get('heat', ''))}' size='12' placeholder='e.g.  carbon'></label>"
            "<button>show</button></form>")  # fmt: skip
    body = [head, form]
    v, why = vector(st, model, prompt, pos, layer, kind)
    if v is None:
        body.append(f"<div class='box bad'>{E(why)}</div>")
    else:
        x = torch.as_tensor(v)[None]
        lgs = {"logit": ro.unembed(x)[0]}
        if layer in ro.lens_layers:
            lgs["jpp"] = ro.lens(x, layer)[0]
        cols = []
        for name, lg in (("J++ lens", lgs.get("jpp")), ("logit lens", lgs["logit"])):
            if lg is None:
                cols.append(f"<div><h3>{name}</h3><p class='mut'>no J++ map at L{layer}</p></div>")
                continue
            top = torch.topk(lg, TOP)
            rows = "".join(f"<tr><td>{i + 1}</td><td>{tk(ro.decode(int(t)))}</td><td>{float(s):.3f}</td></tr>"
                           for i, (t, s) in enumerate(zip(top.indices, top.values, strict=True)))  # fmt: skip
            cols.append(
                f"<div><h3>{name}: top {TOP}</h3><table><tr><th>#</th><th>token</th><th>logit</th></tr>{rows}</table></div>"
            )
        body.append(f"<div class='box'><p><b>{E(VECTOR_TEXT[kind])}</b>{' of ' + prompt if kind == 'state' else ''} at "
                    f"token {pos} ({E(ro.decode(int(ids[pos])))}), L{layer}; norm {float(v.norm()):.2f}</p>"
                    f"<div class='cols'>{''.join(cols)}</div></div>")  # fmt: skip
        listed = listed_tokens(it, ro.tok)
        typed_rows = typed_tokens(typed, ro.tok)
        trs = []
        for label, tids, note in [(lbl, t, n) for lbl, t, n in typed_rows] + [(lbl, t, "") for lbl, t in listed]:
            cells = []
            for name in ("jpp", "logit"):
                lg = lgs.get(name)
                r, t = rank_of(lg, tids) if lg is not None else (None, None)
                cells.append(
                    f"<td>{r if r is not None else '–'}{(' ' + tk(ro.decode(t))) if t is not None and len(tids) > 1 else ''}</td>"
                )
            trs.append(
                f"<tr><td>{E(label)}{(' <span class=mut>' + E(note) + '</span>') if note else ''}</td>{''.join(cells)}</tr>"
            )
        body.append("<div class='box'><h3>Ranks (1 = top; a word's best token)</h3><table><tr><th>token</th><th>J++ lens</th>"
                    f"<th>logit lens</th></tr>{''.join(trs)}</table><p class='mut'>Typed tokens first, then the tokens always "
                    "listed: both bridge words (spellings, symbol; and with their first pieces), every item of the scene, "
                    "both readers' O and S answers (digit, number word).</p></div>")  # fmt: skip
    if q.get("heat"):
        got = typed_tokens(q["heat"], ro.tok)
        if got:
            label, tids, note = got[0]
            body.append(heat_html(st, model, prompt, kind, int(tids[0]), label, note, ro))
    body.append(atoms_html(st, it, model, pos_default, model_layer(model)))
    body.append(checks_html(st, it, model))
    body.append(notes_html(it, view_id, item_id, q, {"prompt": prompt, "pos": pos, "layer": layer, "vector": kind}))
    return doc("".join(body))


def heat_html(st, model, prompt, kind, token, label, note, ro) -> str:
    parts = []
    for lens_name in ("jpp", "logit"):
        h = heatmap(st, model, prompt, kind, lens_name, token)
        roles = st["meta"]["roles_O" if prompt == "O" or kind != "state" else "roles_S"]
        ids = st["ids_O"] if prompt == "O" or kind != "state" else st["ids_S"]
        head = "".join(f"<th>{la}</th>" for la in h["layers"])
        rows = []
        for p in h["positions"]:
            g = h["grid"].get(str(p), {})
            cells = "".join(f"<td style='background:{heat_color(g.get(str(la)), ro.w_u.shape[0])}' title='L{la}'>"
                            f"{g.get(str(la), '')}</td>" for la in h["layers"])  # fmt: skip
            rows.append(
                f"<tr><td>{p}: {tk(ro.decode(int(ids[p])))} <span class='mut'>{E(', '.join(roles.get(str(p), [])))}</span></td>{cells}</tr>"
            )
        parts.append(f"<h4>{'J++ lens' if lens_name == 'jpp' else 'logit lens'} ({h['seconds']} s)</h4><div class='wrap'>"
                     f"<table class='heat'><tr><th>token \\ layer</th>{head}</tr>{''.join(rows)}</table></div>")  # fmt: skip
    return (f"<div class='box'><h3>Rank of {E(label)} by token x layer: {E(VECTOR_TEXT[kind])}"
            f"{' of ' + prompt if kind == 'state' else ''}</h3>{('<p class=mut>' + E(note) + '</p>') if note else ''}"
            + "".join(parts) + "</div>")  # fmt: skip


def atoms_html(st, it, model, pos, layer) -> str:
    atoms = atoms_at(st, it, model, pos, layer)
    if not atoms:
        return "<div class='box'>No atoms at L and the bridge word.</div>"
    rows = "".join(f"<tr><td>{a['rank']}</td><td>{tk(a['token'])}</td><td>{a['coef']:+.3f}</td><td>{a['share']:.4f}</td>"
                   f"<td>{E(a['class'])} <span class='mut'>({E(a['x52_class'])})</span></td></tr>" for a in atoms)  # fmt: skip
    share = sum(a["share"] for a in atoms)
    return (f"<div class='box'><h3>The 25 atoms of the change at L{layer} and the bridge word</h3><table><tr><th>OMP rank</th>"
            f"<th>token</th><th>coefficient (+: toward S)</th><th>energy share</th><th>class (x52_atoms')</th></tr>{rows}"
            f"</table><p class='mut'>Their energy shares sum to {share:.3f} (the J++ part's share of the change).</p></div>")  # fmt: skip


def checks_html(st, it, model) -> str:
    rows = check_51_12(st, it, model) + check_x52(st, it, model)
    if not rows:
        return "<div class='box mut'>Self-checks: no 51.12 or x52_atoms row for this item.</div>"
    trs = "".join(f"<tr><td>{E(r['check'])}</td><td>{r['panel']}</td><td>{r['stored']}</td>"
                  f"<td class='{'ok' if r['ok'] else 'bad'}'>{'equal' if r['ok'] else 'DIFFERS'}</td></tr>" for r in rows)  # fmt: skip
    return f"<div class='box'><h3>Self-checks</h3><table><tr><th>check</th><th>panel</th><th>stored</th><th></th></tr>{trs}</table></div>"


def notes_html(it, view_id, item_id, q, where) -> str:
    prev = "".join(f"<li>{E(r.get('utc', '')[:16])} {E(json.dumps(r.get('where', {})))}: {E(r.get('note', ''))}</li>"
                   for r in jspace_notes(item_id))  # fmt: skip
    return (f"<div class='box'><h3>Note</h3><form method='post' action='/jspace/note'>"
            f"<input type='hidden' name='view' value='{E(view_id)}'><input type='hidden' name='item' value='{E(item_id)}'>"
            f"<input type='hidden' name='seed' value='{E(q.get('seed', '29'))}'>"
            + "".join(f"<input type='hidden' name='{k}' value='{E(str(v))}'>" for k, v in where.items())
            + "<input type='text' name='note' size='80' placeholder='e.g. identity token in the rest at L14'>"
            "<button>save to review/marks.jsonl</button></form>"
            f"<ul>{prev}</ul></div>")  # fmt: skip


def doc(body: str) -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>J-space inspector</title><style>{CSS}</style>"
            f"</head><body><main>{body}</main></body></html>")  # fmt: skip


def note(form: dict[str, str], commit: str) -> dict:
    """A free-text note on an item, in review/marks.jsonl beside the verdict marks: same fields, kind "jspace", no
    verdict (verdict readers skip kind == "jspace")."""
    if not form.get("item") or not form.get("view") or not form.get("note", "").strip():
        raise ValueError("a note needs view, item and text")
    row = {"view": form["view"], "item": form["item"], "seed": int(form.get("seed") or 29), "verdict": None,
           "note": form["note"].strip(), "kind": "jspace",
           "where": {k: form.get(k) for k in ("prompt", "pos", "layer", "vector")}, "commit": commit,
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
    append_line(MARKS, row)
    return row


def with_links(page_html: str) -> str:
    """The dashboard's view page with a "Look into J-space" link on every item card (before its mark form)."""
    pat = re.compile(r"<form class='marks'[^>]*><input type='hidden' name='view' value='([^']*)'>"
                     r"<input type='hidden' name='item' value='([^']*)'>")  # fmt: skip

    def link(m: re.Match) -> str:
        q = urlencode({"view": html.unescape(m.group(1)), "item": html.unescape(m.group(2))})
        return f"<p><a href='/jspace?{q}'>Look into J-space</a></p>" + m.group(0)

    return pat.sub(link, page_html)


# ---- item 3: the automatic rank check ------------------------------------------------------------------------------

KINDS = {"S's bridge (word or symbol)": ("S_bridge_word",), "S's bridge (with first pieces)": ("S_bridge_pieces",),
         "the lookup's S answer (digit or word)": ("PP_S_answer_digit", "PP_S_answer_word"),
         "the recall's S answer (digit or word)": ("PM_S_answer_digit", "PM_S_answer_word")}  # fmt: skip
FLAG_GAP = 0.20


def best(ranks: dict, keys: tuple[str, ...]) -> int | None:
    got = [ranks[k] for k in keys if ranks.get(k) is not None]
    return min(got) if got else None


def rank_table(rows: list[dict]) -> list[dict]:
    """Per (model, view, condition) and token kind: n, the share of items with the token in the top 50 of the readout
    of the J++ part, the rest and the random part, and Dan's flag: the rest's share minus the random part's >= 0.20."""
    groups: dict[tuple, list[dict]] = collections.defaultdict(list)
    for r in rows:
        groups[(r["model"], r["view"], r.get("condition") or "all")].append(r)
        if r.get("condition"):
            groups[(r["model"], r["view"], "all")].append(r)
    out = []
    for (m, v, c), rs in sorted(groups.items()):
        for kind, keys in KINDS.items():
            vals = {p: [best(r["ranks"][p], keys) for r in rs] for p in ("jpp", "rest", "rand")}
            n = sum(x is not None for x in vals["rest"])
            if not n:
                continue
            share = {p: sum(x is not None and x <= TOP50 for x in xs) / n for p, xs in vals.items()}
            med = {p: float(np.median([x for x in xs if x is not None])) for p, xs in vals.items()}
            gap = share["rest"] - share["rand"]
            out.append({"model": m, "view": v, "condition": c, "kind": kind, "n": n, "top50": share, "median": med,
                        "rest_minus_rand": gap, "flag": gap >= FLAG_GAP - 1e-9})  # fmt: skip
    return out


def latest_rank_rows() -> tuple[list[dict], dict[str, str]]:
    """Every model's newest states run's rank_check.jsonl (results/review_states/<run>/)."""
    runs: dict[str, tuple[str, Path]] = {}
    for d in sorted((REPO / "results" / "review_states").glob("*/manifest.json")):
        m = json.loads(d.read_text())
        f = d.parent / "rank_check.jsonl"
        if f.exists():
            key = m["model"]["target"]
            if key not in runs or m["written_utc"] > runs[key][0]:
                runs[key] = (m["written_utc"], f)
    rows = []
    for model, (_, f) in runs.items():
        rows += [{**json.loads(line), "model": model} for line in f.read_text().splitlines() if line.strip()]
    return rows, {m: str(f.parent.relative_to(REPO)) for m, (_, f) in runs.items()}


def jread_rank_rows(model: str) -> list[dict]:
    """Item 3 on the conflict test from 51.10's cached states (x51_jread states.npz: the lookup's O / S at the bridge
    word, P1, at L): Δ, X0's fit over the CPU letter dictionary (x52_atoms.cpu_dictionary), X0's random part, and the
    ranks the GPU job computes (CPU readout). The conflict test's items: 51.10's cases are the X0 main run's."""
    import torch

    from scripts import review_states as RS
    from scripts import statement_positions as SP
    from scripts import x0_necessity as X
    from scripts import x51_jread as JR
    from scripts import x52_atoms as AT

    src = next((r for r in (REPO / "results" / "x51_jread" / JR.RUNS[model], main_checkout() / "results" / "x51_jread" /
                            JR.RUNS[model]) if (r / JR.STATES_FILE).exists()), None)  # fmt: skip
    if src is None:
        raise FileNotFoundError(f"{model}: no 51.10 states.npz")
    layer = model_layer(model)
    z = np.load(src / JR.STATES_FILE)
    layers = [int(x) for x in z["layers"]]
    li, p1 = layers.index(layer), JR.POS.index("P1")
    h = z["h"][:, 0, :, p1, li].astype(np.float32)  # [n, O/S, d]: the lookup's prompts
    cases = X.read_jsonl(src / "cases.jsonl")
    x = torch.tensor(h[:, 1] - h[:, 0])
    ro = readout(model)
    old = pins.TARGET
    try:
        pins.TARGET = model
        _, dic, _ = AT.cpu_dictionary(ro.tok, model, layer)
    finally:
        pins.TARGET = old
    jpp = X.fit(dic, x, X.K_MAIN, "signed")
    del dic
    share = jpp.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    rand = SP.random_subspace_part(
        x, share, SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer))
    )
    parts = {"jpp": jpp, "rest": x - jpp, "rand": rand}
    by_scene = {it["scene"]: it for it in I.items("main_swap", model) if it["reader"] == "PP"}
    rows = []
    for i0 in range(0, len(cases), 32):
        lg = {k: ro.lens(v[i0 : i0 + 32], layer) for k, v in parts.items()}
        for j, c in enumerate(cases[i0 : i0 + 32]):
            it = by_scene.get(c["scene"])
            if it is None:  # not in the conflict test's item set
                continue
            case = it["case"]
            dom = case.get("domain")
            toks = {f"{who}_bridge_{k}": ids for who, name in (("S", case["cf_bridge"]), ("O", case["bridge"]))
                    for k, ids in RS.variant_tokens(ro.tok, name, dom).items()}  # fmt: skip
            for w, r in case["readers"].items():
                for k, ids in RS.answer_tokens(ro.tok, r["cf_answer"], r.get("tok_b")).items():
                    toks[f"{w}_S_answer_{k}"] = ids
            rows.append({"view": "main_swap", "key": c["scene"], "scene": c["scene"], "condition": None, "layer": layer,
                         "share": float(share[i0 + j]), "model": model, "source": "51.10 states (CPU)",
                         "ranks": {k: {t: rank_of(lg[k][j], ids)[0] for t, ids in toks.items()} for k in parts}})  # fmt: skip
    return rows


SECTION = "## J-space rank checks (inspector)"


def rank_section(rows: list[dict], sources: dict[str, str], note: str = "") -> str:
    table = rank_table(rows)
    flags = [t for t in table if t["flag"]]
    label = {m: I.spec()["models"][m]["label"] for m in I.spec()["models"]}
    lines = [SECTION, "",
             "Dan 11:45 (jobs/c3/batch53.yaml inspector_1145 item 3), verbatim: \"Automatic check over every item of the "
             "conflict test and the routes test (not only the sample), at L and the bridge word, results in "
             "docs/verify_pack.md: the rank of S's bridge token (and its variants) in the readout of the J++ part, of the "
             "rest and of a random part of the same share; the share of items with it in the top 50 for each. Flag if the "
             "rest puts it in the top 50 on >= 20% of items more often than the random part does. The same for the answer "
             "words. No rule change: this is a check.\"", "",
             "As computed (scripts/review_jspace.py rank-check): the readout is the J++ lens (JLens.readout) at L; the J++ "
             "part is X0's 25-atom signed OMP over the J++ letter-token atoms, the rest = Δ minus it, the random part X0's "
             "(seed 888 + L) at the J++ part's share; rank = 1 + tokens with a strictly larger logit, a word's best token "
             "(S's bridge: its one-token spellings and symbol, then also the first pieces of split spellings; an answer: "
             "its digit and its number word). Flag read as: (share in the top 50 under the rest) minus (under the random "
             f"part) >= {FLAG_GAP:.2f}. Routes: per condition and over all. "
             + (f"Sources: {'; '.join(f'{label.get(m, m)}: `{s}`' for m, s in sorted(sources.items()))}. " if sources else "")
             + note, "",
             f"**Flags: {len(flags)}**" + (": " + "; ".join(f"{label.get(t['model'], t['model'])} {t['view']} "
                                                             f"{t['condition']}, {t['kind']} (rest {t['top50']['rest']:.2f} vs "
                                                             f"random {t['top50']['rand']:.2f})" for t in flags) if flags else "."),
             "", "| model | test | condition | token | n | top 50: J++ part | rest | random part | rest - random | flag | "
             "median rank: J++ / rest / random |", "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in table:
        s, md = t["top50"], t["median"]
        lines.append(f"| {label.get(t['model'], t['model'])} | {t['view']} | {t['condition']} | {t['kind']} | {t['n']} | "
                     f"{s['jpp']:.2f} | {s['rest']:.2f} | {s['rand']:.2f} | {t['rest_minus_rand']:+.2f} | "
                     f"{'FLAG' if t['flag'] else ''} | {md['jpp']:.0f} / {md['rest']:.0f} / {md['rand']:.0f} |")  # fmt: skip
    return "\n".join(lines) + "\n"


def put_section(text: str) -> None:
    """docs/verify_pack_jspace.md (this check's own file) and the same section in docs/verify_pack.md, replaced in place
    (up to the next '## ' heading) or appended. Docs, not review/ or cache/: the CLI writes them, never the panel."""
    (REPO / "docs" / "verify_pack_jspace.md").write_text(text)
    pack = REPO / "docs" / "verify_pack.md"
    old = pack.read_text() if pack.exists() else "# Verification pack\n"
    if SECTION in old:
        a = old.index(SECTION)
        nxt = old.find("\n## ", a + len(SECTION))
        new = old[:a] + text + (old[nxt + 1 :] if nxt >= 0 else "")
    else:
        new = old.rstrip("\n") + "\n\n" + text
    pack.write_text(new)


def stage_rank_check(from_jread: tuple[str, ...] = ()) -> str:
    rows, sources = latest_rank_rows()
    note = ""
    for m in from_jread:
        if m in sources:
            continue
        rows += jread_rank_rows(m)
        sources[m] = "51.10's cached states (results/x51_jread, CPU; conflict test only)"
        note = "Models read from 51.10's states: the conflict test only, until their states job lands. "
    text = rank_section(rows, sources, note)
    put_section(text)
    print(text)
    return text


def stage_selfcheck() -> list[dict]:
    """51.12's and x52_atoms' checks on every sample item with states."""
    from scripts import review_states as RS

    out = []
    for v in RS.tier1_views():
        for m in I.spec()["models"]:
            if not (STATES / m).exists():
                continue
            items, _ = RS.sample_items(v, m)
            for it in items:
                st = states(m, v["id"], it["id"])
                if st is None:
                    continue
                for r in check_51_12(st, it, m) + check_x52(st, it, m):
                    out.append({"view": v["id"], "item": it["id"], **r})
                    print(json.dumps(out[-1]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["rank-check", "selfcheck", "page"])
    ap.add_argument("--from-jread", default="", help="rank-check: models to read from 51.10's states (comma-separated)")
    ap.add_argument("--view")
    ap.add_argument("--item")
    a = ap.parse_args()
    if a.stage == "rank-check":
        stage_rank_check(tuple(m for m in a.from_jread.split(",") if m))
    elif a.stage == "selfcheck":
        stage_selfcheck()
    else:
        print(page({"view": a.view, "item": a.item}))


if __name__ == "__main__":
    main()
