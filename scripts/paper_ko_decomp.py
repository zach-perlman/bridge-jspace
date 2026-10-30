"""paper_ko_decomp (Zach, 2026-10-30, prereg amendment 68 note 45): which named word the J-space knock-out needs, on
the paper's own lens-eval items.

Sets (copied unchanged from safety-research/jpp_lens@93f02cd data/jlens/evaluations/, whose multihop file is
byte-identical to data/lens_eval_multihop.json; sha256-pinned below):
  ML  lens-eval-multilingual, 107 items; intermediates = [language L, relation R, input in English I, output in English E]
  MH  lens-eval-multihop, 93 items; bridge B = intermediates[0]
  OO  lens-eval-order-ops, 55 items; intermediates = [partial result P, operation O]; descriptive only
Gate (per item): the prompt as note 39 feeds it (trailing space stripped; exp02's prompt_text), greedy 6 tokens
(model.generate), normalised prefix match: NFKC, lower case, leading whitespace and quotes dropped from the continuation;
the target must start it and be followed by a non-alphanumeric character or the end. Chat prefill (exp02's) for a
primary set (ML, MH) only if fewer than 50 of its items are raw-eligible in a full run; OO stays raw.
Read: the target's first token in context (the prompt's ids, then the target's; a lone-space first token joins the
prompt, as ablate_v2 does for digit answers); strict top-1 (argmax over the vocabulary) and log p, delta log p against
the same batch's unedited forward (ablate_v2's reads). Analysis set (reader): gated items whose unedited read is right.
Conditions, ablate_v2's machinery (imported unchanged: ablate.removal_edit with keep_span, ablate_v2.answer_span_edit,
pca_dictionaries, SEED_ROT, top_k), every position, TF32 on, at note 39's main band (27B L24-40, 9B L8-16,
Lightning L20-33):
  paper10, paper10_rot, paper10_pcasize, unembed10        ablate_v2's (protected: the clean top-10 tokens' rows)
  keep_X           paper10 with keep_span = span of the unit J++ vectors of word X's tokens (QR, as ablate_v2's
                   kept_span); X in T (target) and ML: E, I, R, L; MH: B; OO: P, O (OO's keeps descriptive, from D1)
  keep_ctl         the same with another item's word of the control kind (ML: E, same relation when possible; MH: B;
                   OO: P), its tokens count-matched to the item's own word of that kind (seeded subsample, or padded
                   with random letter tokens); Random('n45ctl:<set>:<item>')
  keepR1..3        the same with random letter-token rows, as many as the largest of the item's keep spans, never an
                   item word's or protected row; Random('n45R<k>:<set>:<item>')
  rm_X, rm_X_rot   answer_span_edit over word X's unit J++ vectors at every position except the final one; X in T,
                   ctl and ML: E, R, L; MH: B
  early window     note 39's arm-1 median-onset window (from the model's stored note 39 run): paper10, paper10_rot,
                   keep_T and keep_E (ML) / keep_B (MH) / keep_P (OO)
Word tokens: the first token of every form (as written, lower case, capitalised; with and without a leading space),
whitespace-only first tokens dropped; for keep/rm spans any token (digits included) via the lens; for the protection log
the letter-token dictionary rows (paper10's). Logged per item and word: protected (a word token among the clean top-10).
ML cognates (E and T share a first-token form) are flagged per tokenizer. Byte-identity check (every full run): on the
first 8 gated MH items, the runner's paper10 and paper10_rot edits equal ablate_v2's recipe (its dictionary, protected
rows, SEED_ROT rotation, top_k) on the same tokens: protected rows, edit outputs on the clean residuals at every band
layer, and the final logits (check.json).

2026-10-30 (prereg amendment 72 note 55, the paper's strengths matched for generic damage): --bands NAME=lo-hi ... runs
note 55 instead of note 45 (note 45's runs above are unchanged without it). Sets ML, MH, OO and PO (lens-eval-poetry,
98 couplets, copied unchanged from the same pinned source; T = intermediates[0], the rhyme word; S = the last alphabetic
word of the couplet's first line, the rhyme source; clusters = T's spelled rhyme, from its last vowel group; PO takes
the chat fallback as ML and MH, a primary set here). Same gate, reads, protection and machinery. Per band (the paper's
medium and heavy, percent of depth taken inward), every position:
  top3, paper10, top30                J++ top-K (ablate_v2's topK: protected = the clean top-10 tokens' rows)
  pca3, pca10, pca30                  ablate_v2's variance dictionary (its pca10 rule, nothing protected)
  unembed10, unembed30                the logit lens's directions (ablate_v2's unembedK, protected)
  unembed100, unembed300              the same (amendment 74: S's fallback dose when PCA cannot bracket)
  paper10_rot, paper10_pcasize        as note 45
  keep_T and keep_E (ML) / keep_B (MH) / keep_S (PO), at the --keep-band only (OO: keep_T)
Logged per row: edit_rel = |edit| / |h| (root of summed squares over the band's layers and every position); per item at
the keep band, the share of paper10's removal energy inside each keep span (E_X) and the span's rank. Byte check on the
first 8 gated MH items at every band: paper10, paper10_rot, top3 and top30 against ablate_v2's recipe. Then the text
stage (scripts/removal_textloss.agreement): plain-text top-1 agreement with the clean model on the 64 pinned WikiText rows
and 64 v4 passages, per band, under removal_textloss.TEXT_CONDS (text_rows.jsonl). Reader: scripts/paper_ko_read55.py.

python scripts/paper_ko_decomp.py --name N --why W [--sets ML MH OO] [--limit K] [--prev39 RUN] [--prompt-end auto]
python scripts/paper_ko_decomp.py --name N --why W --sets ML MH OO PO --bands medium=17-24 heavy=14-27 [--keep-band medium]
python scripts/paper_ko_decomp.py --check        (CPU: data hashes, tokenizer, words, cognates, plan)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import time
import unicodedata
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402

EXP = "paper_ko_decomp"
RES = pins.RESULTS_DIR / EXP
DATA = {
    "ML": ("lens_eval_multilingual.json", "fa70b9bd89416a6d8d985a80dc628b109ae6fd3b25b9275c0fc5065d7ff4a0ef"),
    "MH": ("lens_eval_multihop.json", "50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416"),
    "OO": ("lens_eval_order_ops.json", "b203206d16ff628152cc86f3838604e06cb54776f3e14fa1c34f150db8bc7560"),
}
WORD_INDEX = {"ML": {"L": 0, "R": 1, "I": 2, "E": 3}, "MH": {"B": 0}, "OO": {"P": 0, "O": 1}}
CTL_KIND = {"ML": "E", "MH": "B", "OO": "P"}
KEEP_WORDS = {"ML": ["T", "E", "I", "R", "L"], "MH": ["T", "B"], "OO": ["T", "P", "O"]}
RM_WORDS = {"ML": ["T", "E", "R", "L"], "MH": ["T", "B"], "OO": ["T"]}
EARLY_KEEP = {"ML": ["T", "E"], "MH": ["T", "B"], "OO": ["T", "P"]}
# note 55: the paper's rhyme set (its words T, S; the per-item word dictionaries above need an entry for any set run)
DATA_PO = {"PO": ("lens_eval_poetry.json", "6aeb3415c5a5c3f3827c9efe63f006de02f5ef39a816bbac68e15e733aba60cc")}
CTL_KIND["PO"], KEEP_WORDS["PO"], RM_WORDS["PO"], EARLY_KEEP["PO"] = "S", ["T", "S"], ["T", "S"], ["T", "S"]
N55_DOSE = ("top3", "paper10", "top30", "pca3", "pca10", "pca30", "unembed10", "unembed30", "paper10_rot", "paper10_pcasize",
            "unembed100", "unembed300")  # the last two: amendment 74
N55_KEEP = {"ML": ["T", "E"], "MH": ["T", "B"], "OO": ["T"], "PO": ["T", "S"]}
N55_BYTE_CONDS = ("paper10", "paper10_rot", "top3", "top30")
MAIN_BAND = {"qwen3.6-27b": (24, 40), "qwen3.5-9b": (8, 16), "nemotron-3.5-lightning": (20, 33)}  # note 39's
N_DRAWS, GATE_TOKENS, CHAT_FALLBACK_BELOW, N_BYTE_CHECK = 3, 6, 50, 8
QUOTES = " \t\n\"'«»“”‘’„"
# MH answer types (the reader's bootstrap clusters), from the targets; digits are "number", single capitals "letter"
MH_TYPE = {"Atlantic": "ocean", "Pacific": "ocean", "Portuguese": "language", "French": "language", "red": "colour",
           "green": "colour", "Asia": "continent", "Europe": "continent", "winter": "season", "wolverine": "animal",
           "Colorado": "us_state", "California": "us_state", "Au": "chemical symbol", "Fe": "chemical symbol",
           "Cu": "chemical symbol", "liquid": "state of matter", "war": "abstract", "beginnings": "abstract",
           "Canada": "country", "Portugal": "country", "Earth": "planet", "Jupiter": "planet", "Saturn": "planet",
           "Mars": "planet", "iron": "element", "silicon": "element", "carbon": "element", "nitrogen": "element",
           "oxygen": "element", "sodium": "element", "sulfur": "element", "aluminum": "element", "magnesium": "element",
           "tellurium": "element", "Moscow": "capital", "Beijing": "capital", "Jakarta": "capital", "Euro": "currency",
           "Caesar": "person", "west": "direction", "down": "direction", "up": "direction", "north": "direction",
           "November": "month", "January": "month", "day": "time of day", "night": "time of day", "peace": "antonym",
           "birth": "antonym", "low": "antonym"}  # fmt: skip


def mh_type(target: str) -> str:
    if target.isdigit():
        return "number"
    if re.fullmatch(r"[A-Z]", target):
        return "letter"
    return MH_TYPE[target]


def load_set(s: str) -> list[dict]:
    name, sha = {**DATA, **DATA_PO}[s]
    raw = (pins.DATA_DIR / name).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    assert got == sha, f"data/{name} sha256 {got} != pinned {sha}"
    items = json.loads(raw)["items"]
    if s == "PO":  # note 55: the couplets have no target field; the rhyme word is
        items = [{**it, "target": it["intermediates"][0]} for it in items]
    return items


def rhyme_source(it: dict) -> str:
    """Note 55's S: the last alphabetic word of the couplet's first line (the prompt's second line)."""
    return re.findall(r"[A-Za-z]+", it["prompt"].split("\n")[1])[-1]


def rhyme_key(word: str) -> str:
    """PO's bootstrap cluster: the word's spelled rhyme, from its last vowel group (y a vowel; a final silent e kept)."""
    w = word.lower()
    core = w[:-1] if len(w) > 2 and w.endswith("e") and w[-2] not in "aeiouy" else w
    m = re.search(r"[aeiouy]+[^aeiouy]*$", core)
    return (m[0] if m else core) + w[len(core) :]


def cluster_of(s: str, it: dict) -> str:
    if s == "PO":
        return rhyme_key(it["target"])
    return {"ML": lambda: it["intermediates"][1], "MH": lambda: mh_type(it["target"]), "OO": lambda: it["intermediates"][1]}[s]()


def words_of(s: str, it: dict) -> dict[str, str]:
    if s == "PO":
        return {"T": it["target"], "S": rhyme_source(it)}
    out = {"T": it["target"]}
    out.update({k: it["intermediates"][i] for k, i in WORD_INDEX[s].items()})
    return out


def forms(word: str) -> list[str]:
    cases = dict.fromkeys([word, word.lower(), word[:1].upper() + word[1:]])
    return [p + c for c in cases for p in ("", " ")]


def word_tokens(tok, word: str) -> list[int]:
    """First token of every form of the word, whitespace-only tokens dropped."""
    out = set()
    for f in forms(word):
        ids = tok(f, add_special_tokens=False).input_ids
        if ids and tok.decode([ids[0]]).strip():
            out.add(ids[0])
    return sorted(out)


def normalise(s: str) -> str:
    return unicodedata.normalize("NFKC", s).lower()


def prefix_match(continuation: str, target: str) -> bool:
    c, t = normalise(continuation).lstrip(QUOTES), normalise(target).strip()
    return bool(t) and c.startswith(t) and (len(c) == len(t) or not c[len(t)].isalnum())


def target_ids(tok, encode, text: str, target: str, sep: str) -> tuple[list[int], int, int, bool]:
    """(prompt ids for the read, the target's first token, the target's token count, whether the boundary was clean):
    the target tokenised after the prompt in context; a whitespace-only first token joins the prompt (ablate_v2's digit
    answers: the prompt then ends in ' ')."""
    p = encode(text)
    full = encode(text + sep + target)
    clean = full[: len(p)] == p
    rest = full[len(p) :] if clean else tok(sep + target, add_special_tokens=False).input_ids
    if rest and not tok.decode([rest[0]]).strip() and len(rest) > 1:
        p, rest = p + rest[:1], rest[1:]
    return p, rest[0], len(rest), clean


# ---- the run --------------------------------------------------------------------------------------------------


class TokenVecs:
    """answer_span_edit's D for any tokens: atoms(ids) = the unit J++ vectors of those token ids at one layer."""

    def __init__(self, lens, layer: int):
        self.lens, self.layer = lens, layer

    def atoms(self, ids: torch.Tensor) -> torch.Tensor:
        return self.lens.vectors(self.layer, ids)


def span(lens, la: int, ids: list[int]) -> torch.Tensor:
    """Orthonormal basis [d, k] of the unit J++ vectors of ids (QR, as ablate_v2's kept_span)."""
    return torch.linalg.qr(lens.vectors(la, torch.tensor(ids, device="cuda")).double().T)[0]


def onset_window(prev39: str | None) -> tuple[int, int] | None:
    if not prev39:
        return None
    from scripts.paper_swap_read import Run

    run = Run(pins.RESULTS_DIR / "paper_swap_decomp" / prev39, n_boot=0)
    w = run.median_onset_window("jpp", run.names("primary"))
    return (int(w.split("-")[0]), int(w.split("-")[1])) if w else None


def conditions(s: str, early: bool) -> list[tuple[str, bool]]:
    """(condition, early window) pairs for one set."""
    main = ["paper10", "paper10_rot", "paper10_pcasize", "unembed10"]
    main += [f"keep_{w}" for w in KEEP_WORDS[s]] + ["keep_ctl"] + [f"keepR{k + 1}" for k in range(N_DRAWS)]
    main += [c for w in RM_WORDS[s] + ["ctl"] for c in (f"rm_{w}", f"rm_{w}_rot")]
    out = [(c, False) for c in main]
    if early:
        out += [(c, True) for c in ["paper10", "paper10_rot"] + [f"keep_{w}" for w in EARLY_KEEP[s]]]
    return out


def conditions55(s: str, bands: dict[str, list[int]], keep_band: str) -> list[tuple[str, str]]:
    """Note 55: (condition, band name) pairs for one set; the keeps at the keep band only."""
    out = []
    for b in bands:
        out += [(c, b) for c in N55_DOSE]
        if b == keep_band:
            out += [(f"keep_{w}", b) for w in N55_KEEP[s]]
    return out


def rel_tracked(e, acc: torch.Tensor):
    """Note 55: the edit e, unchanged, with sum ||edit||^2 and sum ||h||^2 per batch row added to acc [B, 2]."""

    def f(h: torch.Tensor) -> torch.Tensor:
        out = e(h)
        acc[:, 0] += (out.double() - h.double()).pow(2).sum((1, 2))
        acc[:, 1] += h.double().pow(2).sum((1, 2))
        return out

    return f


def parse_bands(spec: list[str]) -> dict[str, list[int]]:
    out = {}
    for x in spec:
        name, rng = x.split("=")
        lo, hi = map(int, rng.split("-"))
        out[name] = list(range(lo, hi + 1))
    return out


@torch.no_grad()
def run(a) -> None:
    from bridge_jspace.ablate import LensDictionary, RowSettings, first_token_logits, removal_edit, rotation
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts.ablate_v2 import PCA_K, SEED_ROT, answer_span_edit, pca_dictionaries, top_k
    from scripts.exp02_swaps import prompt_text

    target = pins.TARGET
    pins.check_run_name(a.name)
    out_dir = RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = True  # ablate_v2's default
    main_band = MAIN_BAND[target]
    early = onset_window(a.prev39)
    band_main = list(range(main_band[0], main_band[1] + 1))
    band_early = list(range(early[0], early[1] + 1)) if early else []
    n55 = bool(a.bands)  # prereg amendment 72 note 55 (its own conditions and bands; note 45's run is unchanged without it)
    bands55 = parse_bands(a.bands) if n55 else {}
    assert not (n55 and early), "note 55 has no early window"
    assert not n55 or a.keep_band in bands55, "--keep-band must name one of --bands"
    sets = {s: load_set(s)[: a.limit or None] for s in a.sets}
    full = not a.limit
    manifest = {
        "exp": EXP, "run": a.name, "why": a.why, "note": "prereg amendment 68 note 45", "target": target, "model": pins.model_pin(),
        "lens": {pins.FROZEN_LENS: list(pins.LENS_SOURCES[pins.FROZEN_LENS])},
        "data": {s: {"file": f"data/{({**DATA, **DATA_PO})[s][0]}", "sha256": ({**DATA, **DATA_PO})[s][1], "n_run": len(v)} for s, v in sets.items()},
        "source": "safety-research/jpp_lens@93f02cd data/jlens/evaluations (copied unchanged)",
        "main_band": f"{main_band[0]}-{main_band[1]}", "early_window": f"{early[0]}-{early[1]}" if early else None,
        "early_from": f"paper_swap_decomp/{a.prev39} (arm 1's median onset, J++)" if early else None,
        "conditions": {s: [c + ("@early" if e else "") for c, e in conditions(s, bool(early))] for s in sets},
        "seeds": {"rotation": f"ablate_v2 SEED_ROT {SEED_ROT} + layer", "ctl": "Random('n45ctl:<set>:<item>')",
                  "keepR": "Random('n45R<k>:<set>:<item>')", "ctl_choice": "Random('n45ctlpick:<set>:<item>')"},
        "gate": f"greedy {GATE_TOKENS} tokens, normalised prefix match; chat_prefill for ML / MH if < {CHAT_FALLBACK_BELOW} raw-eligible (full runs)",
        "tf32": True, "bj_gram_proj": __import__("os").environ.get("BJ_GRAM_PROJ"),
        "command": " ".join(sys.argv), "git_state": pins.git_state(), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }  # fmt: skip
    if n55:
        from scripts.removal_textloss import TEXT_CONDS

        manifest.update({"note": "prereg amendment 72 note 55", "main_band": None,
                         "bands": {b: f"{v[0]}-{v[-1]}" for b, v in bands55.items()}, "keep_band": a.keep_band,
                         "conditions": {s: [f"{c}@{b}" for c, b in conditions55(s, bands55, a.keep_band)] for s in sets},
                         "byte_check": {"conditions": list(N55_BYTE_CONDS), "bands": list(bands55), "items": f"first {N_BYTE_CHECK} gated MH"},
                         "text": None if a.no_text else {"conditions": list(TEXT_CONDS), "n_per_set": a.limit or 64, "sets": ["wiki", "v4"],
                                                         "code": "scripts/removal_textloss.agreement"},
                         "po_rule": "T = intermediates[0]; S = last alphabetic word of the couplet's first line; cluster = T's spelled rhyme",
                         "force_chat": a.force_chat})  # fmt: skip
    elif a.force_chat:
        manifest["force_chat"] = a.force_chat
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    letters = model.letter_token_ids()
    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    row_of = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
    row_of[letters] = torch.arange(letters.numel(), device="cuda")
    layers = sorted(set(band_main) | set(band_early)) if not n55 else sorted(set().union(*bands55.values()))
    dic = {la: LensDictionary(wg, lens.J(la)) for la in layers}
    rot = {la: rotation(wg.shape[1], SEED_ROT + la) for la in layers}
    unembed = LensDictionary(wg, torch.eye(wg.shape[1], device="cuda"))
    pca = pca_dictionaries(model, band_main if not n55 else layers)
    encode = lambda text: model.encode(text)[0].tolist()  # noqa: E731
    print(f"[{a.name}] loaded {time.time() - t0:.0f}s; main {band_main[0]}-{band_main[-1]}, early {early}"
          + (f"; note 55 bands {manifest['bands']}" if n55 else ""), flush=True)  # fmt: skip

    # gate
    def gate(s: str, prompt_end: str) -> list[dict]:
        out = []
        for it in sets[s]:
            text = prompt_text(tok, it["prompt"], prompt_end)
            ids = model.encode(text)
            _, cont, _ = model.generate(ids, GATE_TOKENS)
            sep = " " if prompt_end == "chat_prefill" or it["prompt"] != it["prompt"].rstrip() else ""
            p_ids, t_first, t_len, clean_b = target_ids(tok, encode, text, it["target"], sep)
            out.append({"set": s, "name": it["name"], "prompt_end": prompt_end, "continuation": cont,
                        "eligible": prefix_match(cont, it["target"]), "ids": p_ids, "tok": t_first, "target_tokens": t_len,
                        "boundary_clean": clean_b, "cluster": cluster_of(s, it)})  # fmt: skip
        return out

    items: list[dict] = []
    decisions = {}
    for s in sets:
        rows = gate(s, "stripped")
        n_raw = sum(r["eligible"] for r in rows)
        decisions[s] = {"raw_eligible": n_raw, "n": len(rows), "prompt_end": "stripped"}
        if (s in ("ML", "MH") or (n55 and s == "PO")) and full and a.prompt_end == "auto" and n_raw < CHAT_FALLBACK_BELOW:
            rows = gate(s, "chat_prefill")
            decisions[s].update(prompt_end="chat_prefill", chat_eligible=sum(r["eligible"] for r in rows))
        elif s in a.force_chat:  # smoke only: a stored full run's chat-prefill decision, reproduced on --limit items
            rows = gate(s, "chat_prefill")
            decisions[s].update(prompt_end="chat_prefill", chat_eligible=sum(r["eligible"] for r in rows), forced=True)
        items += rows
    print(f"[{a.name}] gate {decisions} {time.time() - t0:.0f}s", flush=True)
    by_name = {(s, it["name"]): it for s in sets for it in sets[s]}

    # per item: words, tokens, cognates, control word
    for r in items:
        it = by_name[(r["set"], r["name"])]
        w = words_of(r["set"], it)
        r["words"] = w
        r["word_tokens"] = {k: word_tokens(tok, v) for k, v in w.items()}
        r["single_token_target"] = r["target_tokens"] == 1
        if r["set"] == "ML":
            r["cognate"] = bool(set(r["word_tokens"]["E"]) & set(r["word_tokens"]["T"]))
        kind = CTL_KIND[r["set"]]
        own_toks = set().union(*r["word_tokens"].values())
        pool = [x for x in items if x["set"] == r["set"] and x["name"] != r["name"]]
        if r["set"] == "ML":  # same relation first
            same = [x for x in pool if by_name[(x["set"], x["name"])]["intermediates"][1] == it["intermediates"][1]]
            pool = same or pool
        cands = sorted({words_of(r["set"], by_name[(x["set"], x["name"])])[kind] for x in pool})
        cands = [c for c in cands if not set(word_tokens(tok, c)) & own_toks]
        r["ctl_word"] = random.Random(f"n45ctlpick:{r['set']}:{r['name']}").choice(cands) if cands else None

    # byte-identity reference: ablate_v2's recipe for paper10 / paper10_rot, batch of one
    ref_cache: dict = {}

    def ref_edits(ids_t, cond, la_list):
        """ablate_v2's main loop for one item, rebuilt independently (its dictionary, row map, rotation, protection)."""
        if not ref_cache:
            lt = model.letter_token_ids()
            w = model.hf.lm_head.weight[lt].float() * model.norm_gain()
            ro = torch.full((model.hf.lm_head.weight.shape[0],), -1, dtype=torch.long, device="cuda")
            ro[lt] = torch.arange(lt.numel(), device="cuda")
            ref_cache.update(row_of=ro, dic={la: LensDictionary(w, lens.J(la)) for la in la_list},
                       rot={la: rotation(w.shape[1], SEED_ROT + la) for la in la_list})  # fmt: skip
        clean = first_token_logits(model, ids_t, {})
        prot = [ref_cache["row_of"][t][ref_cache["row_of"][t] >= 0] for t in clean.topk(10, dim=1).indices][0]
        rs = [RowSettings(skip=[], protected=prot)]
        return {la: removal_edit("top", ref_cache["dic"][la], rs, rotation=ref_cache["rot"][la] if cond.endswith("_rot") else None, k=top_k(cond))
                for la in la_list}, prot  # fmt: skip

    def make_edits(cond: str, chunk: list[dict], protected: list[torch.Tensor], band: list[int], energy=None) -> dict:
        """The per-layer edits of one condition for a batch of items (rows in chunk order). Note 55: with energy
        ([len(chunk), 1 + keeps]), paper10's removal energy and its part in each of the item's keep spans are summed."""
        edits = {}
        for la in band:
            if cond in ("top3", "top30", "pca3", "pca10", "pca30", "unembed30", "unembed100", "unembed300"):  # note 55's doses (ablate_v2's
                # topK, pcaK, unembedK; unembed100 / 300: amendment 74); removal_edit chunks rows itself above K = 100
                pc = cond.startswith("pca")  # its pca rule: nothing protected (the rows index principal directions)
                rs = [RowSettings(skip=[], protected=None if pc else protected[i]) for i in range(len(chunk))]
                d = pca[la] if pc else unembed if cond.startswith("unembed") else dic[la]
                edits[la] = removal_edit("top", d, rs, k=top_k(cond))
                continue
            obs = None
            if energy is not None and cond == "paper10":

                def obs(r, B, T, la=la):  # read-only (removal_edit's observe): the removal before any keep / rotation
                    for b in range(B):
                        rb = r[b * T : (b + 1) * T].double()
                        energy[b, 0] += rb.pow(2).sum()
                        for j, w in enumerate(N55_KEEP[chunk[b]["set"]], 1):
                            energy[b, j] += (rb @ span(lens, la, chunk[b]["word_tokens"][w])).pow(2).sum()

            if cond.startswith("rm_"):  # answer_span_edit over the word's unit J++ vectors, every position but the last
                word = cond.split("_")[1]
                rows = [torch.tensor(r["word_tokens"][word], device="cuda") for r in chunk]
                outside = [[len(r["ids"]) - 1] for r in chunk]
                edits[la] = answer_span_edit(TokenVecs(lens, la), rows, outside, rotation=rot[la] if cond.endswith("_rot") else None)
                continue
            rs = [RowSettings(skip=[], protected=protected[i]) for i in range(len(chunk))]
            keep = None
            if cond.startswith("keep"):  # paper10 with the word's span kept out of its removal (note 37's keep_span)
                word = cond[len("keep_"):] if cond.startswith("keep_") else cond[len("keep"):]
                keep = [span(lens, la, r["word_tokens"][word]) for r in chunk]
            d = unembed if cond == "unembed10" else dic[la]
            edits[la] = removal_edit("top", d, rs, rotation=rot[la] if cond.endswith("_rot") else None,
                                     k=top_k("unembed10" if cond == "unembed10" else "paper10"),
                                     size_match=pca[la].D[:PCA_K] if cond.endswith("_pcasize") else None, keep_span=keep,
                                     observe=obs)  # fmt: skip
        return edits

    rows_out: list[dict] = []
    elig = [r for r in items if r["eligible"]]
    groups: dict = {}
    for r in elig:
        groups.setdefault((r["set"], len(r["ids"])), []).append(r)
    log_items = []
    for (s, _), group in sorted(groups.items()):
        for b0 in range(0, len(group), a.batch):
            chunk = group[b0 : b0 + a.batch]
            ids_t = torch.tensor([r["ids"] for r in chunk], device="cuda")
            answer = torch.tensor([r["tok"] for r in chunk], device="cuda")
            clean = first_token_logits(model, ids_t, {})
            clean_lp = clean.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
            top10 = clean.topk(10, dim=1).indices
            protected = [row_of[t][row_of[t] >= 0] for t in top10]
            for i, r in enumerate(chunk):
                prot_rows = set(protected[i].tolist())
                top_set = set(top10[i].tolist())
                r["clean_correct"] = int(clean[i].argmax()) == r["tok"]
                r["clean_logp"] = float(clean_lp[i])
                rows_out.append({"set": s, "name": r["name"], "window": "-", "cond": "none", "correct": r["clean_correct"],
                                 "logp": r["clean_logp"], "dlogp": 0.0, "top_id": int(clean[i].argmax())})  # fmt: skip
                # control and random keep tokens (count-matched), drawn now that the protected rows are known
                kind = CTL_KIND[s]
                n_kind = len(r["word_tokens"][kind])
                own_toks = set().union(*r["word_tokens"].values())
                rng = random.Random(f"n45ctl:{s}:{r['name']}")
                ctl = word_tokens(tok, r["ctl_word"]) if r["ctl_word"] else []
                ctl = sorted(rng.sample(ctl, n_kind)) if len(ctl) > n_kind else ctl
                if len(ctl) < n_kind:
                    lt = letters.tolist()
                    padpool = sorted(set(lt) - own_toks - set(ctl) - {lt[j] for j in prot_rows})
                    ctl = ctl + rng.sample(padpool, n_kind - len(ctl))
                r["word_tokens"]["ctl"] = ctl
                n_r = max(len(r["word_tokens"][k]) for k in KEEP_WORDS[s] + ["ctl"])
                lt = letters.tolist()
                rpool = sorted(set(lt) - own_toks - set(ctl) - {lt[j] for j in prot_rows})
                for k in range(N_DRAWS):
                    r["word_tokens"][f"R{k + 1}"] = sorted(random.Random(f"n45R{k + 1}:{s}:{r['name']}").sample(rpool, n_r))
                # protection log: a word token among the clean top-10 tokens / a word row among paper10's protected rows
                wl = {k: [int(row_of[t]) for t in v if int(row_of[t]) >= 0] for k, v in r["word_tokens"].items()}
                r["protected"] = {k: bool(set(v) & top_set) for k, v in r["word_tokens"].items()}
                r["protected_rows"] = {k: bool(set(wl[k]) & prot_rows) for k in wl}
                log_items.append(r)
            if not n55:
                plan = [(c, "early" if e else "main", band_early if e else band_main) for c, e in conditions(s, bool(early))]
            else:
                plan = [(c, b, bands55[b]) for c, b in conditions55(s, bands55, a.keep_band)]
                energy = torch.zeros(len(chunk), 1 + len(N55_KEEP[s]), dtype=torch.float64, device="cuda")
                for i, r in enumerate(chunk):
                    r["n_protected_rows"] = int(protected[i].numel())
                    r["rank55"] = {w: len(r["word_tokens"][w]) for w in N55_KEEP[s]}
            for cond, wname, band in plan:
                rel, tc = None, time.time()
                if not n55:
                    edits = make_edits(cond, chunk, protected, band)
                else:
                    edits = make_edits(cond, chunk, protected, band, energy if (cond == "paper10" and wname == a.keep_band) else None)
                    rel = torch.zeros(len(chunk), 2, dtype=torch.float64, device="cuda")
                    edits = {la: rel_tracked(e, rel) for la, e in edits.items()}
                logits = first_token_logits(model, ids_t, edits)
                lp = logits.log_softmax(-1).gather(1, answer[:, None]).squeeze(1)
                for i, r in enumerate(chunk):
                    rows_out.append({"set": s, "name": r["name"], "window": wname, "cond": cond,
                                     "correct": int(logits[i].argmax()) == r["tok"], "logp": float(lp[i]),
                                     "dlogp": float(lp[i] - clean_lp[i]), "top_id": int(logits[i].argmax())})  # fmt: skip
                    if rel is not None:
                        rows_out[-1]["edit_rel"] = float((rel[i, 0] / rel[i, 1]).sqrt())
                if rel is not None:  # note 55: the batch's wall time for this condition (GPU synced by the reads above)
                    for x in rows_out[-len(chunk) :]:
                        x["sec"] = round(time.time() - tc, 3)
            if n55:
                for i, r in enumerate(chunk):
                    e = energy[i].tolist()
                    r["E55"] = {w: (e[j] / e[0] if e[0] > 0 else None) for j, w in enumerate(N55_KEEP[s], 1)}
        print(f"[{a.name}] {s}: length group of {len(group)} items done {time.time() - t0:.0f}s", flush=True)

    # byte-identity check on the first N_BYTE_CHECK gated MH items (batch of one, both recipes)
    check: dict = {"items": [], "all_equal": None}
    mh = [r for r in elig if r["set"] == "MH"][:N_BYTE_CHECK]
    for r in mh if not n55 else []:
        ids_t = torch.tensor([r["ids"]], device="cuda")
        _, rec = model.run(ids_t, record=tuple(band_main))
        clean = first_token_logits(model, ids_t, {})
        prot = row_of[clean.topk(10, dim=1).indices[0]]
        prot = prot[prot >= 0]
        res = {"name": r["name"]}
        for cond in ("paper10", "paper10_rot"):
            mine = make_edits(cond, [r], [prot], band_main)  # the runner's own construction
            theirs, prot_ref = ref_edits(ids_t, cond, band_main)
            res[f"{cond}_protected_equal"] = bool(torch.equal(prot, prot_ref))
            res[f"{cond}_edit_equal_all_layers"] = all(bool(torch.equal(mine[la](rec[la][None]), theirs[la](rec[la][None]))) for la in band_main)
            res[f"{cond}_logits_equal"] = bool(torch.equal(first_token_logits(model, ids_t, mine), first_token_logits(model, ids_t, theirs)))
        check["items"].append(res)
    for bname, band in bands55.items():  # note 55: every band, its J top-K conditions against ablate_v2's recipe
        ref_cache.clear()  # the reference dictionaries are built for the band's layers
        for r in mh:
            ids_t = torch.tensor([r["ids"]], device="cuda")
            _, rec = model.run(ids_t, record=tuple(band))
            clean = first_token_logits(model, ids_t, {})
            prot = row_of[clean.topk(10, dim=1).indices[0]]
            prot = prot[prot >= 0]
            res = {"name": r["name"], "band": bname}
            for cond in N55_BYTE_CONDS:
                mine = make_edits(cond, [r], [prot], band)
                theirs, prot_ref = ref_edits(ids_t, cond, band)
                res[f"{cond}_protected_equal"] = bool(torch.equal(prot, prot_ref))
                res[f"{cond}_edit_equal_all_layers"] = all(bool(torch.equal(mine[la](rec[la][None]), theirs[la](rec[la][None]))) for la in band)
                res[f"{cond}_logits_equal"] = bool(torch.equal(first_token_logits(model, ids_t, mine), first_token_logits(model, ids_t, theirs)))
            check["items"].append(res)
    check["all_equal"] = all(v for x in check["items"] for k, v in x.items() if k not in ("name", "band")) if check["items"] else None
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    print(f"[{a.name}] byte-identity check on {len(mh)} MH items: all equal {check['all_equal']}", flush=True)

    keys = ("set", "name", "prompt_end", "continuation", "eligible", "tok", "target_tokens", "single_token_target", "boundary_clean",
            "cluster", "words", "ctl_word", "word_tokens", "cognate", "protected", "protected_rows", "clean_correct", "clean_logp",
            "n_protected_rows", "rank55", "E55")  # fmt: skip  # the last three: note 55 only
    with open(out_dir / "items.jsonl", "w") as f:
        for r in items:
            f.write(json.dumps({k: r[k] for k in keys if k in r}, ensure_ascii=False) + "\n")
    with open(out_dir / "rows.jsonl", "w") as f:
        for r in rows_out:
            f.write(json.dumps(r) + "\n")
    summary = {"gate": decisions, "eligible": {s: sum(r["eligible"] for r in items if r["set"] == s) for s in sets},
               "clean_correct": {s: sum(bool(r.get("clean_correct")) for r in items if r["set"] == s) for s in sets},
               "rows": len(rows_out), "byte_check_all_equal": check["all_equal"], "seconds": round(time.time() - t0),
               "reader": f"python scripts/paper_ko_read.py results/{EXP}/{a.name}"}  # fmt: skip
    if n55:
        summary["reader"] = f"python scripts/paper_ko_read55.py results/{EXP}/{a.name}"
        summary["note"] = "prereg amendment 72 note 55"
        summary["command"], summary["git_state"] = manifest["command"], manifest["git_state"]
        if not a.no_text:  # the text stage: plain-text top-1 agreement (Fig. 22's metric), per band and condition
            from scripts.removal_textloss import TEXT_CONDS, agreement, v4_texts, wiki_texts

            n_text = a.limit or 64
            vt, vids = v4_texts(tok, n_text)
            trows = []
            for tname, texts in (("wiki", wiki_texts(tok, n_text)), ("v4", vt)):
                for x in agreement(model, texts, bands55, TEXT_CONDS, dic, unembed, pca, rot, row_of, batch=a.text_batch):
                    trows.append({"textset": tname, **x, **({"id": vids[x["text"]]} if tname == "v4" else {})})
                print(f"[{a.name}] text {tname}: {len(texts)} texts done {time.time() - t0:.0f}s", flush=True)
            with open(out_dir / "text_rows.jsonl", "w") as f:
                for x in trows:
                    f.write(json.dumps(x) + "\n")
            agg: dict = {}
            for x in trows:
                k = f"{x['textset']}/{x['band']}/{x['cond']}"
                agg.setdefault(k, [0, 0])
                agg[k][0] += x["agree"]
                agg[k][1] += x["n"]
            summary["text_agreement"] = {k: round(v[0] / v[1], 4) for k, v in agg.items()}
            summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


# ---- --check: CPU dry run ---------------------------------------------------------------------------------------


def check() -> None:
    from bridge_jspace.tokens import load_tokenizer

    tok = load_tokenizer()
    print(f"{pins.TARGET}: main band {MAIN_BAND.get(pins.TARGET)}")
    for s in DATA:
        its = load_set(s)
        n_single, cognates, bad_boundary, words_ok, clusters = 0, [], 0, 0, {}
        for it in its:
            text = it["prompt"].rstrip()
            sep = "" if it["prompt"] == text else " "
            enc = lambda t: tok(t, add_special_tokens=False).input_ids  # noqa: E731
            _, _, n_t, clean_b = target_ids(tok, enc, text, it["target"], sep)
            n_single += n_t == 1
            bad_boundary += not clean_b
            w = words_of(s, it)
            wt = {k: word_tokens(tok, v) for k, v in w.items()}
            words_ok += all(wt.values())
            if s == "ML" and set(wt["E"]) & set(wt["T"]):
                cognates.append(it["name"])
            c = cluster_of(s, it)
            clusters[c] = clusters.get(c, 0) + 1
        print(f"  {s}: {len(its)} items (sha ok); single-token targets {n_single}; every word has tokens {words_ok}; "
              f"unclean target boundary {bad_boundary}; clusters {len(clusters)}")
        if s == "ML":
            print(f"  ML cognates (E and T share a first-token form): {len(cognates)} {cognates}")
        print(f"  {s} conditions: {len(conditions(s, True))} ({len(conditions(s, False))} at the main band)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--sets", nargs="+", default=["ML", "MH", "OO"], choices=list(DATA) + list(DATA_PO))
    ap.add_argument("--limit", type=int, default=0, help="first K items per set (smoke)")
    ap.add_argument("--prev39", help="the model's note 39 run (its arm-1 median-onset window is the early window)")
    ap.add_argument("--prompt-end", default="auto", choices=["auto", "stripped"])
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--bands", nargs="*", default=[], help="note 55: NAME=lo-hi ... (runs note 55 instead of note 45)")
    ap.add_argument("--keep-band", default="medium", help="note 55: the band of the keep conditions")
    ap.add_argument("--no-text", action="store_true", help="note 55: skip the plain-text agreement stage")
    ap.add_argument("--text-batch", type=int, default=16)
    ap.add_argument("--force-chat", nargs="*", default=[], help="smoke only: gate these sets with the chat prefill")
    args = ap.parse_args()
    if args.check:
        check()
    else:
        assert args.name and args.why
        run(args)
