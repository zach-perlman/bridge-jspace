"""x51_answer (batch 51, test 51.12; jobs/c3/batch51.yaml addendum_4, design and rules fixed in advance; Q51.12 in
predictions/2026-10-28_dan.md): is it the bridge or the answer that moves through the lens? The answer-direction control
on three sets, each with its own items, gate, layer, change and read (imported, unchanged):

  z2   Zach's never-named bridge (x50_zach --part z2): the change at the description's last token, per reader (K = lookup,
       M = recall: the K and M passages differ before it, so each reader has its own Δ); 9B L12, 27B L32. Items: the
       stored run's chosen passages (x50_zach.RUNS["z2"]), rebuilt on the tokenizer by x50_zach.encode and checked id by
       id; read: x50_zach's (the top token after the prompt, no prefill, against the answer's first token).
  e1   the main test (x0_necessity; X0's items, gate and chat read): the change at the bridge word, one Δ from the
       lookup's prompts (both readers' prompts agree through it); 9B L12, 27B L32, Muse L26. Items: the stored X0 run's
       (x45b_binding.MAIN_RUN, the runs 49.1 / 48.1 used) chat items at L, rebuilt by x0_necessity.build_cases and
       checked id by id.
  cue  47.3's described bridge in locker scenes (x47_cue): the change at the cue token, one Δ from the lookup's
       prompts; 9B L12, 27B L32. Items: the stored run's chosen scenes (x47_cue.RUNS), rebuilt by x47_cue.scenes from its
       kept cues and checked id by id; the lookup's switch is x47_cue's (it follows the change: identity, position or
       value).

The gate is each source run's (asserted from its gate.json; a failed gate means "not tested").

Answer directions A (per item): the J++ lens atoms (JLens.vectors(L, ids), unit rows: the very rows of the dictionary
X0's OMP uses for letter tokens, and of X0's digit dictionary "jppdig" for digit tokens; not the unembedding) of the
first token of each answer word and of its obvious variants (leading space, capitalised; a variant whose first token is
whitespace only, e.g. " 5" -> " ", is dropped). Answer words: z2 O's and S's answers (the same for K and M); e1 both
readers' answers on O and S (digits); cue the recall's O / S answers (legs) and the lookup's four route digits (A's
locker a = O's answer, B's b, C's c and the new e = S's answer: x47_cue's lookup switch counts b, c and e). P_A = the
orthogonal projector on span(A) (SVD of the atoms, rank kept above 1e-6 of the top singular value).

Parts of Δ = h_S - h_O at the edited token at L: P_J Δ = X0's 25-atom signed OMP part over the J++ letter-token atoms
(x0_necessity.fit, the stored runs' path); (I - P_A) P_J Δ = the J++ part with A projected out ("remove only the lens
directions that are not answer directions": the J++ part's component in span(A) is kept in the state, everything else
of the J++ part is removed); P_A Δ = the answer directions alone. Arms (each added at the edited token at L on O,
X0's AddRows), each against a random part of its own share (x6_routes.removal_arms: statement_positions.
random_subspace_part over X0's random basis, seed 888 + L, the same basis for every arm):

  whole             Δ
  no_jpp            Δ - P_J Δ                 arm 1 (as run; must reproduce the stored runs' no_jpp / no_part)
  no_jpp_rand       Δ - R(P_J Δ's share)
  no_jpp_A          Δ - (I - P_A) P_J Δ       arm 2
  no_jpp_A_rand     Δ - R((I - P_A) P_J Δ's share)
  no_A              Δ - P_A Δ                 arm 3
  no_A_rand         Δ - R(P_A Δ's share)      arm 4 ("without a random part of A's share" = arm 3's random twin)

Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader (switch: the set's own). Rules (fixed in
advance, per model and reader; point estimates decide, EPS 1e-9 at the bars; cluster bootstrap over the bridge entity,
10,000 resamples, seed 0, paired): "the lens effect is the entity": e2 >= 0.7 e1 and e3 <= 0.10; "the lens effect is the
answer": e2 <= 0.3 e1 and e3 >= 0.5 e1; else mixed (both shares e2 / e1 and e3 / e1 reported); e1 <= 0 or undefined:
can't tell. Beside (descriptive): per item how many of Δ's 25 OMP atoms are answer atoms (0 by construction where every
answer token is a digit: the letter dictionary has no digit token); the lens readout at the edited token on O and on S
(top-1 over the vocabulary: own answer / own bridge entity / neither; per reader's answer separately, the lookup's digit
at the bridge word reported on its own); arm 1 against the stored runs item by item (agreement.json).

SEALED: the run writes per-item outputs and the arm-1 agreement only; verdict and view refuse until
predictions/2026-10-28_dan.md holds Dan's Q51.12 answer at HEAD.

uv run python scripts/x51_answer.py plan --set e1                                          # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x51_answer.py run --set e1 --name qwen35_9b_x51_12_e1   # GPU (sealed)
uv run python scripts/x51_answer.py verdict                                                 # CPU, after Q51.12
uv run python scripts/x51_answer.py view                                                    # CPU, after Q51.12
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import loaded_hub_kernels, switches
from scripts import x0_necessity as X
from scripts import x48_heads as H

EXP = "x51_answer"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch51.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q51.12"
SETS = ("z2", "e1", "cue")
SET_TEXT = {"z2": "Z2 (Zach's never-named bridge, the description's last token)",
            "e1": "the main test E1 (the bridge word)", "cue": "47.3's described bridge (the cue token, locker scenes)"}  # fmt: skip
RUNS = {
    "z2": {"qwen3.5-9b": "qwen35_9b_x51_12_z2", "qwen3.6-27b": "x51_12_z2_27b"},
    "e1": {"qwen3.5-9b": "qwen35_9b_x51_12_e1", "qwen3.6-27b": "x51_12_e1_27b", "muse-glimmer-30b": "muse30_x51_12_e1"},
    "cue": {"qwen3.5-9b": "qwen35_9b_x51_12_cue", "qwen3.6-27b": "x51_12_cue_27b"},
}
TAGS = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse"}
SPEC_IDS = {s: {t: f"x51_12_{s}_{TAGS[t]}" for t in RUNS[s]} for s in SETS}
ARMS = ("whole", "no_jpp", "no_jpp_rand", "no_jpp_A", "no_jpp_A_rand", "no_A", "no_A_rand")
PAIRS = {1: ("no_jpp", "no_jpp_rand"), 2: ("no_jpp_A", "no_jpp_A_rand"), 3: ("no_A", "no_A_rand")}
ARM_TEXT = {
    "whole": "Δ = h_S - h_O at the edited token at L",
    "no_jpp": "arm 1: Δ - P_J Δ (P_J Δ: X0's 25-atom signed OMP part over the J++ letter-token atoms at L)",
    "no_jpp_A": "arm 2: Δ - (I - P_A) P_J Δ (the J++ part with the answer directions A projected out)",
    "no_A": "arm 3: Δ - P_A Δ (the answer directions alone)",
    "*_rand": "each arm's random twin: Δ minus X0's random subspace part of the removed part's share of ||Δ||^2 (seed "
              "888 + L); no_A_rand is arm 4, 'without a random part of A's share'",
}  # fmt: skip
ENTITY_KEEP, ENTITY_A_MAX = 0.7, 0.10
ANSWER_KEEP, ANSWER_A_MIN = 0.3, 0.5
EPS = 1e-9
N_PROMPTS, N_ROWS, VIEW_SEED = 5, 10, 0
RANK_TOL = 1e-6
LABELS = {"entity": "the lens effect is the entity", "answer": "the lens effect is the answer", "mixed": "mixed",
          "na": "can't tell (arm 1 has no extra loss beyond random)"}  # fmt: skip
RULE = ('Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1\'s extra loss and arm 3 '
        'costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone '
        "costs >= 0.5 of arm 1. Else: mixed, report both shares.")  # fmt: skip
AS_COMPUTED = (
    "Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader over the source run's items (switch: the "
    "set's own read; 47.3's lookup: follows the change, identity / position / value). e1, e2, e3 = arms 1, 2, 3; arm 4 "
    "(no_A_rand) is arm 3's random twin. 'Keeps >= 0.7 of arm 1' = e2 / e1 >= 0.7; 'costs <= 0.10 beyond random' = e3 "
    "<= 0.10; 'falls to <= 0.3 of arm 1' = e2 / e1 <= 0.3; 'costs >= 0.5 of arm 1' = e3 / e1 >= 0.5. Point estimates "
    "decide (EPS 1e-9); e1 <= 0 or undefined (no switch under the whole change) -> can't tell; CIs from X0's cluster "
    "bootstrap over the bridge entity (10,000, seed 0), paired across arms (ratios on the same draws). Decisive cells for "
    "Q51.12: Z2 both readers; E1 the recall (the lookup beside); 47.3 both readers. Projected out: (I - P_A) P_J Δ, P_A "
    "the orthogonal projector on the span of the item's answer atoms (not: dropping answer atoms from the OMP fit, which "
    "would leave arm 2 = arm 1 whenever no answer atom is among the 25, always so for digit answers)."
)  # fmt: skip
READER_NAME = {"PP": "lookup", "PM": "recall", "K": "lookup", "M": "recall"}
ALNUM = re.compile(r"[^\W_]")  # a letter or a digit
LETTER = re.compile(r"[^\W\d_]")  # bridge_jspace.model._HAS_LETTER: the OMP dictionary's tokens


# ---- answer directions and parts (CPU-testable) --------------------------------------------------------------------


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def variant_ids(tok, words: list[str]) -> list[int]:
    """The first token of each word and of its obvious variants (leading space, capitalised), whitespace-only or
    letterless-and-digitless first tokens dropped; sorted, unique."""
    from scripts import suite_v1 as S

    out = set()
    for w in words:
        w = str(w)
        for v in dict.fromkeys((w, " " + w, cap(w), " " + cap(w))):
            ids = S.ids(tok, v)
            if ids and ALNUM.search(tok.decode([ids[0]])):
                out.add(int(ids[0]))
    return sorted(out)


def answer_basis(vecs):
    """An orthonormal basis [d, r] of the span of the rows of vecs [m, d] (SVD in float64 on the CPU, singular values
    above RANK_TOL x the largest kept); [d, 0] for no rows."""
    import torch

    v = vecs.detach().double().cpu()
    if v.shape[0] == 0:
        return torch.zeros(v.shape[1], 0, dtype=torch.float32)
    u, s, _ = torch.linalg.svd(v.T, full_matrices=False)
    keep = s > RANK_TOL * s.max()
    return u[:, keep].float()


def answer_parts(delta, pj, bases: list) -> tuple[Any, Any]:
    """Per row i of Δ [n, d] with basis Q_i [d, r_i]: (I - P_A) P_J Δ (the J++ part with A projected out) and P_A Δ."""
    import torch

    pja, pa = torch.empty_like(pj, dtype=torch.float32), torch.empty_like(delta, dtype=torch.float32)
    for i, q in enumerate(bases):
        q = q.to(delta.device, torch.float32)
        pja[i] = pj[i].float() - q @ (q.T @ pj[i].float())
        pa[i] = q @ (q.T @ delta[i].float())
    return pja, pa


def omp_support(dic, x, k: int):
    """exp04_brew_parts.signed_omp's greedy selection, returning the chosen atom indices [m, k] and the approximation
    (signed_omp returns only the approximation; the run asserts the two approximations agree)."""
    import torch

    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    for _ in range(k):
        scores = ((x - approx) @ dic.T).abs()
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dic[chosen].double()
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
    return chosen, approx


def all_arms(delta, pj, bases: list, basis) -> tuple[dict, dict]:
    """The seven arms (ARMS order) and the per-row shares of the three removed parts (x6_routes.removal_arms: each part
    removed and, against it, X0's random part of its own share)."""
    from scripts import x6_routes as R

    pja, pa = answer_parts(delta, pj, bases)
    more, sh = R.removal_arms(delta, {"jpp": pj, "jpp_A": pja, "A": pa}, basis)
    arms = {"whole": delta, **more}
    assert tuple(arms) == ARMS, tuple(arms)
    sh["A_in_jpp"] = (pj.float() - pja).norm(dim=-1) ** 2 / (delta.float().norm(dim=-1) ** 2).clamp_min(1e-30)
    return arms, sh


# ---- items: each set's own code, rebuilt and checked against the stored run (tokenizer only) -----------------------


def layer_of(set_name: str, target: str) -> int:
    from scripts import x50_zach as Z

    return Z.LAYERS[target][0] if set_name == "z2" else X.PREDICTED[target]


def source_of(set_name: str, target: str) -> Path:
    from scripts import x45b_binding as B
    from scripts import x47_cue as CUE
    from scripts import x50_zach as Z

    if set_name == "z2":
        return Z.RESULTS / Z.RUNS["z2"][target]
    if set_name == "e1":
        return X.RESULTS / B.MAIN_RUN[target]
    return CUE.RESULTS / CUE.RUNS[target]


def unit(set_name: str, c: dict, key: str, entity: str, cf_entity: str, extra_words: dict[str, list[str]]) -> dict:
    """One item in this script's shape: per reader its prompts, edited position, answer tokens, read suffix and the
    reader whose prompts give its Δ (z2: its own; e1 / cue: the lookup's, identical through the edited token)."""
    readers = {}
    for w, rd in c["readers"].items():
        pos = rd["pos"] if set_name == "z2" else c["pos"]
        src = w if set_name == "z2" else X.LOOKUP
        readers[w] = {**{k: v for k, v in rd.items() if k not in ("context", "cf_context")}, "pos": pos, "src": src,
                      "suffix": [] if set_name == "z2" else c["space"],
                      "words_A": [rd["answer"], rd["cf_answer"], *extra_words.get(w, [])]}  # fmt: skip
    out = {
        "set": set_name,
        "key": key,
        "scene": c["scene"],
        "entity": entity,
        "cf_entity": cf_entity,
        "readers": readers,
    }
    if set_name == "cue":
        out["route_tokens"] = c["route_tokens"]
        out["expect"] = c["expect"]
    if set_name == "z2":
        out["source_set"] = c["set"]
        out["desc"], out["cf_desc"] = c["desc"], c["cf_desc"]
    return out


def z2_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    from scripts import x50_zach as Z

    src = source_of("z2", target)
    gate = json.loads((src / "gate.json").read_text())
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert layer_of("z2", target) in m["layers"], f"{src.name} has no L{layer_of('z2', target)}"
    stored = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    passages = {}
    for s in sorted({s for s, _ in gate["order"]}):
        ps, _ = Z.load_pairs(s, "z2")
        passages.update({(s, p[Z.LOOKUP]["scene"]): p for p in ps})
    items, drops = [], collections.Counter()
    for s, scene in gate["order"]:
        old = stored[(s, scene)]
        c, why = Z.encode(tok, "z2", passages[(s, scene)], old["cf_bridge"], old["cf_desc"])
        assert c is not None, f"{s} {scene}: does not rebuild ({why})"
        c["set"] = s
        for w in Z.READERS:
            assert c["readers"][w]["ids"] == old["readers"][w]["ids"], f"{scene}: {w}'s ids changed since {src.name}"
            assert c["readers"][w]["pos"] == old["readers"][w]["pos"], f"{scene}: {w}'s patch token moved"
        c["desc"], c["cf_desc"] = old["desc"], old["cf_desc"]
        items.append(unit("z2", c, f"{s}|{scene}", c["bridge"], c["cf_bridge"], {}))
    g = {"pass": bool(gate["pass"]), "chosen": gate["chosen"], "org_read_accuracy": gate["org_read_accuracy"],
         "gate": gate["gate"]}  # fmt: skip
    return items, g, {"source": src.name, "items": len(items), "drops": dict(drops),
                      "sets": dict(collections.Counter(it["source_set"] for it in items))}  # fmt: skip


def e1_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    from scripts import x45b_binding as B
    from scripts import x47_cumulative as C

    src = source_of("e1", target)
    layer = layer_of("e1", target)
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["predicted"] == layer, f"{src.name}: layer {m['predicted']}, not {layer}"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {src.name}"
    scenes, _ = C.stored_whole(src, layer)
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    with B.x0_alt(m.get("alt") or "cf", ("chat",)):
        cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    items = []
    for s in scenes:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the bridge position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        it = unit("e1", c, s, c["bridge"], c["cf_bridge"], {})
        it["domain"] = c["domain"]
        items.append(it)
    gate = json.loads((src / "gate.json").read_text())["gate"]["chat"]
    g = {"pass": bool(gate["pass"]) and bool(gate["enough"]), "chosen": len(items),
         "org_read_accuracy": gate["org_accuracy"], "gate": X.GATE, "eligible": gate["eligible"]}  # fmt: skip
    return items, g, {"source": src.name, "set": m["set"], "items": len(items)}


def cue_items(tok, target: str) -> tuple[list[dict], dict, dict]:
    from scripts import x47_cue as CUE

    src = source_of("cue", target)
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["layer"] == layer_of("cue", target), f"{src.name}: layer {m['layer']}"
    cues = json.loads((src / "cues.json").read_text())
    gate = json.loads((src / "gate.json").read_text())
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    cases, _ = CUE.scenes(tok, cues["kept"])
    rebuilt = {c["scene"]: c for c in cases}
    items = []
    for s in gate["order"]:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the cue position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        routes = [str(c["expect"][k]) for k in ("identity", "position")]  # a (original) and e (value) are O's / S's
        items.append(unit("cue", c, s, c["bridge"], c["cf_bridge"], {X.LOOKUP: routes}))
    g = {"pass": bool(gate["pass"]) and cues["status"] == "ok", "chosen": gate["chosen"],
         "org_read_accuracy": gate["org_read_accuracy"], "gate": gate["gate"]}  # fmt: skip
    return items, g, {"source": src.name, "items": len(items), "cues_kept": len(cues["kept"])}


BUILD = {"z2": z2_items, "e1": e1_items, "cue": cue_items}


def item_tokens(tok, it: dict) -> dict:
    """Per item: A's token ids (every reader's answer words with variants), and per variant (org / alt) the own answer
    tokens of each reader and the own bridge entity's tokens (for the lens readout)."""
    a_ids = variant_ids(tok, [w for rd in it["readers"].values() for w in rd["words_A"]])
    own = {"org": {w: variant_ids(tok, [rd["answer"]]) for w, rd in it["readers"].items()},
           "alt": {w: variant_ids(tok, [rd["cf_answer"]]) for w, rd in it["readers"].items()}}  # fmt: skip
    bridge = {"org": variant_ids(tok, [it["entity"]]), "alt": variant_ids(tok, [it["cf_entity"]])}
    return {"A": a_ids, "A_letter": [t for t in a_ids if LETTER.search(tok.decode([t]))], "own": own, "bridge": bridge}


def size_summary(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": int(min(values)), "median": float(np.median(values)), "max": int(max(values)),
            "mean": round(float(np.mean(values)), 3), "hist": dict(sorted(collections.Counter(values).items()))}  # fmt: skip


def mark(decode, ids: list[int], pos: int) -> str:
    return decode(ids[:pos]) + "⟦" + decode(ids[pos : pos + 1]) + "⟧" + decode(ids[pos + 1 :])


def stage_plan(set_name: str, plan_dir: str | None = None, k_prompts: int = N_PROMPTS) -> Path:
    """Tokenizer and stored runs only: the items (rebuilt and checked against the source run), the source gate, |A| per
    item (token count; letter atoms of them), the arms and reads, and k rendered prompts (seed 0)."""
    from bridge_jspace.utils import git_state
    from scripts import x45m

    target = pins.TARGET
    assert target in RUNS[set_name], f"51.12 {set_name} runs on {sorted(RUNS[set_name])}, not {target}"
    tok = x45m.tokenizer()
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    items, gate, counts = BUILD[set_name](tok, target)
    toks = [item_tokens(tok, it) for it in items]
    sizes = [len(t["A"]) for t in toks]
    letters = [len(t["A_letter"]) for t in toks]
    a_decoded = collections.Counter(decode([t]) for tk in toks for t in tk["A"])
    reads = len(items) * len(next(iter(items))["readers"]) * (1 + len(ARMS)) if items else 0
    out = Path(plan_dir) if plan_dir else RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=True)
    chosen = sorted(random.Random(VIEW_SEED).sample(range(len(items)), min(k_prompts, len(items))))
    blob = {"set": set_name, "target": target, "layer": layer_of(set_name, target), "run": RUNS[set_name][target],
            "spec": SPEC_IDS[set_name][target], "code": git_state(), "source_gate": gate, "counts": counts,
            "entities": len({it["entity"] for it in items}), "arms": list(ARMS), "reads": reads,
            "delta_forwards": len(items) * 2 * len({rd["src"] for rd in items[0]["readers"].values()}) if items else 0,
            "A_tokens_per_item": size_summary(sizes), "A_letter_tokens_per_item": size_summary(letters),
            "A_tokens_most_common": a_decoded.most_common(30),
            "answer_atoms_in_omp_25": "needs Δ (GPU forwards; no states of these items are cached): reported by the run "
                                      "(norms.jsonl n_answer_atoms_in_25); 0 by construction for a digit-only A (the "
                                      "letter dictionary holds no digit token)"
                                      if letters and max(letters) else "0 by construction: no answer token of these "
                                      "items is a letter token, and OMP's dictionary is the letter tokens",
            "prompts": [{"key": items[i]["key"], "bridge": f"{items[i]['entity']} -> {items[i]['cf_entity']}",
                         "A": [decode([t]) for t in toks[i]["A"]],
                         **{f"{READER_NAME[w]}_{v}": mark(decode, rd["ids"][v] + rd["suffix"], rd["pos"])
                            for w, rd in items[i]["readers"].items() for v in ("org", "alt")}} for i in chosen]}  # fmt: skip
    stem = f"plan-{set_name}-{TAGS[target]}"
    (out / f"{stem}.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    lines = [f"# {EXP} plan: {SET_TEXT[set_name]} on {target} (tokenizer and stored runs only; UNVERIFIED)", "",
             f"Source {counts['source']}, L{blob['layer']}, gate {gate}; items {len(items)} ({blob['entities']} bridge "
             f"entities); reads {reads}; |A| tokens per item {blob['A_tokens_per_item']}; letter atoms per item "
             f"{blob['A_letter_tokens_per_item']}.", "",
             "Answer tokens (most common): " + ", ".join(f"{t!r} x{n}" for t, n in blob["A_tokens_most_common"]), ""]  # fmt: skip
    for p in blob["prompts"]:
        lines += [f"## {p['key']}: {p['bridge']}; A = {p['A']}", ""]
        for k, v in p.items():
            if k.endswith(("_org", "_alt")):
                lines += [f"{k}:", "", "```", v, "```", ""]
    (out / f"{stem}.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in blob.items() if k not in ("prompts", "code")}, indent=1, ensure_ascii=False))
    print("wrote", out / stem, flush=True)
    return out


# ---- GPU -----------------------------------------------------------------------------------------------------------


def rank_of(logits, t: int) -> int:
    return int((logits > logits[t]).sum()) + 1


def readout_row(it: dict, toks: dict, src: str, v: str, logits, digit_ids: list[int]) -> dict:
    """The lens readout at the edited token of one prompt (v: org / alt) from one source reader's state: top-1, its
    class (own answer / own bridge / neither), whose answer it is, the other prompt's answer or bridge, and the ranks of
    each reader's own answer token (over the vocabulary and among the digits)."""
    other = "alt" if v == "org" else "org"
    top = int(logits.argmax())
    own_ans = {w: top in ids for w, ids in toks["own"][v].items()}
    is_ans, is_bridge = any(own_ans.values()), top in toks["bridge"][v]
    dl = logits[digit_ids]
    ranks, drank = {}, {}
    for w, rd in it["readers"].items():
        t = int(rd["tok_A"] if v == "org" else rd["tok_b"])
        ranks[w] = rank_of(logits, t)
        if t in digit_ids:
            drank[w] = int((dl > logits[t]).sum()) + 1
    return {"key": it["key"], "entity": it["entity"], "source": src, "variant": v, "top": top,
            "class": "answer" if is_ans else "bridge" if is_bridge else "neither", "both": bool(is_ans and is_bridge),
            "own_answer_of": [w for w, x in own_ans.items() if x],
            "other_answer": any(top in ids for ids in toks["own"][other].values()),
            "other_bridge": top in toks["bridge"][other], "answer_rank": ranks, "answer_digit_rank": drank,
            "bridge_rank": min((rank_of(logits, t) for t in toks["bridge"][v]), default=None),
            "top_digit": int(digit_ids[int(dl.argmax())])}  # fmt: skip


def switch_of(set_name: str, reader: str, row: dict) -> int:
    """The set's switch: 47.3's lookup follows the change (identity / position / value); otherwise the top token is S's
    answer's first token."""
    from scripts import x47_cue as CUE

    if set_name == "cue" and reader == X.LOOKUP:
        return int(row["route"] in CUE.FOLLOW)
    return int(row["switched"])


def read_item(model, set_name: str, it: dict, layer: int, arms: dict, i: int, digits, ws) -> list[dict]:
    """Every arm (and O unedited) on the item's O prompt, each reader, with the set's own read and route."""
    import torch

    from scripts import x6_routes as R
    from scripts import x50_zach as Z
    from scripts.exp04_brew_parts import AddRows

    rows = []
    for w, rd in it["readers"].items():
        edits = [{}] + [{layer: AddRows(arms[rd["src"]][a][i : i + 1], [rd["pos"]])} for a in ARMS]
        logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", rd["suffix"], ws)
        if set_name == "z2":
            cands = torch.tensor(sorted({rd["tok_A"], rd["tok_b"], *([rd["tok_lure"]] if rd["tok_lure"] else [])}),
                                 device=model.device)  # fmt: skip
        else:
            cands = digits
        for a, lg in zip(("none", *ARMS), logits, strict=True):
            row = X.read_row(lg, rd, cands)
            if set_name == "z2":
                row["route"] = Z.route(row["top"], rd)
            elif set_name == "cue" and w == X.LOOKUP:
                row["route"] = R.classify(row["top"], it)
            else:
                row["route"] = None
            rows.append({"key": it["key"], "scene": it["scene"], "entity": it["entity"], "reader": w, "arm": a,
                         **row, "sw": switch_of(set_name, w, row)})  # fmt: skip
    return rows


def stored_rows(set_name: str, src: Path, layer: int) -> dict[tuple[str, str, str], dict]:
    """The source run's rows of the arms this run repeats (none, whole, no_jpp, no_jpp_rand), keyed (key, reader,
    arm), with the set's switch."""
    out = {}
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if set_name == "e1":
            if r["rendering"] != "chat" or r["layer"] != layer:
                continue
            if r["arm"] in ("none", "whole"):
                arm = r["arm"]
            elif (r["dict"], r["k"], r["omp"]) == ("jpp", X.K_MAIN, "signed") and r["arm"] in ("no_part", "no_rand"):
                arm = {"no_part": "no_jpp", "no_rand": "no_jpp_rand"}[r["arm"]]
            else:
                continue
            key = r["scene"]
        else:
            if set_name == "z2" and r["layer"] != layer:
                continue
            if r["arm"] not in ("none", "whole", "no_jpp", "no_jpp_rand"):
                continue
            arm, key = r["arm"], (f"{r['set']}|{r['scene']}" if set_name == "z2" else r["scene"])
        # the 9B's X0 run (24 Oct) predates the stored top token: None there, and agree_top counts what is stored
        out[(key, r["reader"], arm)] = {"switched": int(r["switched"]), "top": r.get("top"),
                                        "sw": switch_of(set_name, r["reader"], r) if set_name == "cue" else int(r["switched"])}  # fmt: skip
    return out


def excess(sw: dict[str, list[int]], arm: str, rand: str) -> float:
    """X0's excess (S_rand - S_arm) / S_whole on point estimates (nan when nothing switched under the whole change)."""
    whole = float(np.mean(sw["whole"]))
    return (float(np.mean(sw[rand])) - float(np.mean(sw[arm]))) / whole if whole > 0 else math.nan


def agreement(set_name: str, rows: list[dict], stored: dict) -> dict:
    """Arm 1 (and none / whole / its random twin) of this run against the stored run, item by item, per reader."""
    out: dict[str, Any] = {}
    readers = sorted({r["reader"] for r in rows})
    for w in readers:
        per: dict[str, Any] = {}
        sw_new: dict[str, list[int]] = {}
        sw_old: dict[str, list[int]] = {}
        for a in ("none", "whole", "no_jpp", "no_jpp_rand"):
            mine = [r for r in rows if r["reader"] == w and r["arm"] == a]
            pairs = [(r["sw"], stored.get((r["key"], w, a)), r["top"]) for r in mine]
            have = [(x, y, t) for x, y, t in pairs if y is not None]
            per[a] = {"n": len(mine), "matched": len(have), "agree_switch": sum(x == y["sw"] for x, y, _ in have),
                      "agree_top": sum(t == y["top"] for _, y, t in have if y["top"] is not None),
                      "top_stored": sum(y["top"] is not None for _, y, _ in have), "rerun": sum(x for x, _, _ in have),
                      "stored": sum(y["sw"] for _, y, _ in have)}  # fmt: skip
            sw_new[a] = [x for x, _, _ in have]
            sw_old[a] = [y["sw"] for _, y, _ in have]
        per["extra_loss_arm1"] = {"rerun": excess(sw_new, "no_jpp", "no_jpp_rand") if sw_new["whole"] else math.nan,
                                  "stored": excess(sw_old, "no_jpp", "no_jpp_rand") if sw_old["whole"] else math.nan}  # fmt: skip
        out[READER_NAME[w]] = per
    return out


def manifest(name: str, set_name: str, target: str, layer: int, src: Path) -> dict:
    from bridge_jspace.utils import git_state
    from scripts import suite_split as SUITE

    files = ("manifest.json", "gate.json", "cases.jsonl", "outcomes.jsonl") + (
        ("cues.json",) if set_name == "cue" else ()
    )
    return {"exp": EXP, "run": name, "test": "51.12", "set": set_name, "set_text": SET_TEXT[set_name],
            "spec": f"jobs/c3/batch51.yaml (addendum_4, 51.12); jobs/c3/{SPEC_IDS[set_name][target]}.yaml",
            "question": f"{QUESTION} ({PREDICTIONS})", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                       for p in (SPEC, *(src / f for f in files)) if p.exists()},
            "source": src.name, "layer": layer, "arms": list(ARMS), "arm_text": ARM_TEXT, "k": X.K_MAIN,
            "omp": "signed", "pairs": {str(k): list(v) for k, v in PAIRS.items()},
            "answer_directions": "JLens.vectors(L, first tokens of the answer words and their variants: leading space, "
                                 "capitalised; whitespace-only first tokens dropped), unit rows; span by SVD (float64, "
                                 f"rank tol {RANK_TOL}); z2 O / S answers; e1 both readers' O / S answers; cue the recall's "
                                 "O / S answers and the lookup's a, b, c, e",
            "projected_out": "(I - P_A) P_J Δ: the J++ part minus its component in span(A)",
            "read": "z2: x50_zach's (top token after the prompt, no prefill); e1 / cue: X0's chat read (top token after "
                    "the digit's space token); 47.3's lookup switch = follows the change (identity / position / value)",
            "delta": "z2: per reader from its own O / S prompts; e1 / cue: from the lookup's prompts",
            "readout": "lens readout (JLens.readout) at the edited token on O and S: top-1 over the vocabulary, class "
                       "own answer / own bridge / neither, ranks",
            "gate": "the source run's (asserted from its gate.json)", "rule": RULE, "as_computed": AS_COMPUTED,
            "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED, "view": VIEW_SEED},
            "order": {"items": "the source run's item order", "reads": f"per item and reader: O unedited then the "
                      f"{len(ARMS)} arms in ARMS order, batches of at most {SUITE.BATCH} rows (BJ_SUITE_BATCH)"},
            "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip


def stage_run(name: str, set_name: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in RUNS[set_name], f"51.12 {set_name} runs on {sorted(RUNS[set_name])}, not {target}"
    layer, src = layer_of(set_name, target), source_of(set_name, target)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = manifest(name, set_name, target, layer, src)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
    items, gate, counts = BUILD[set_name](tok, target)
    toks = [item_tokens(tok, it) for it in items]
    tested = gate["pass"] and bool(items)
    (out / "plan.json").write_text(json.dumps(counts, indent=1) + "\n")
    X.write_jsonl(out / "cases.jsonl", [{**it, "tokens": tk} for it, tk in zip(items, toks, strict=True)])
    (out / "gate.json").write_text(json.dumps({"source": src.name, "gate": gate, "tested": tested,
                                              "order": [it["key"] for it in items],
                                              "hub_kernels": loaded_hub_kernels()}, indent=1) + "\n")  # fmt: skip
    if not tested:
        print("not tested: the source run's gate failed or no items; see gate.json", flush=True)
        return out
    ws = X.whitespace_mask(model)
    digit_list = X.digit_ids(tok)
    digits = torch.tensor(digit_list, device=dev)
    sources = sorted({rd["src"] for it in items for rd in it["readers"].values()})
    with torch.no_grad():
        # Δ per source reader and the lens readout of O's and S's states at the edited token
        deltas: dict[str, list] = {s: [] for s in sources}
        readout = []
        for it, tk in zip(
            progress(items, f"51.12 {set_name}: Δ and the lens readout at L{layer} (item)"), toks, strict=False
        ):
            for s in sources:
                rd = it["readers"][s]
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][rd["pos"]].float().clone()
                     for v in ("org", "alt")}  # fmt: skip
                deltas[s].append(h["alt"] - h["org"])
                for v in ("org", "alt"):
                    lg = lens.readout(h[v][None], layer)[0].float()
                    readout.append(readout_row(it, tk, s, v, lg, digit_list))
        X.write_jsonl(out / "readout.jsonl", readout)
        letters = model.letter_token_ids()
        jdic = lens.vectors(layer, letters).to(dev)
        pos_of = {int(t): i for i, t in enumerate(letters.tolist())}
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(dev)
        bases = [answer_basis(lens.vectors(layer, torch.tensor(tk["A"], dtype=torch.long, device=dev))) for tk in toks]
        arms, norms = {}, []
        for s in sources:
            x = torch.stack(deltas[s]).to(dev)
            pj = X.fit(jdic, x, X.K_MAIN, "signed").to(dev)  # the stored runs' path (arm 1)
            chosen, approx = omp_support(jdic, x, X.K_MAIN)
            assert torch.allclose(approx, pj, atol=1e-4 * float(pj.abs().max()) + 1e-6), "OMP support does not match"
            arms[s], sh = all_arms(x, pj, bases, basis)
            for i, (it, tk) in enumerate(zip(items, toks, strict=True)):
                a_pos = {pos_of[t] for t in tk["A"] if t in pos_of}
                hits = [int(letters[j]) for j in chosen[i].tolist() if j in a_pos]
                norms.append({"key": it["key"], "entity": it["entity"], "source": s, "norm": round(float(x[i].norm()), 4),
                              **{f"share_{k}": round(float(v[i]), 6) for k, v in sh.items()},
                              "A_tokens": len(tk["A"]), "A_rank": int(bases[i].shape[1]), "A_ids": tk["A"],
                              "A_letter_tokens": len(tk["A_letter"]), "n_answer_atoms_in_25": len(hits),
                              "answer_atoms_in_25": hits})  # fmt: skip
        del jdic
        torch.cuda.empty_cache()
        X.write_jsonl(out / "norms.jsonl", norms)
        rows = []
        for i, it in enumerate(progress(items, f"51.12 {set_name}: {len(ARMS)} arms + O x readers at L{layer} (item)")):
            rows += read_item(model, set_name, it, layer, arms, i, digits, ws)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    agree = agreement(set_name, rows, stored_rows(set_name, src, layer))
    (out / "agreement.json").write_text(json.dumps(agree, indent=1) + "\n")
    print(json.dumps(agree, indent=1), flush=True)
    m["items"] = len(items)
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU, sealed) -----------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q51.12 at `rev` (x48_heads.parse_answer: 'Dan:' / 'Dan (27B):' lines and bullet
    continuations), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    return H.parse_answer(text, QUESTION)


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def ok(z: float | None) -> bool:
    return z is not None and not math.isnan(z)


def rule(e1: float, e2: float, e3: float) -> dict:
    """The rules fixed in advance on point estimates (EPS at the bars)."""
    if not ok(e1) or e1 <= EPS:
        return {"label": LABELS["na"], "key": "na", "share2": math.nan, "share3": math.nan, "entity": False,
                "answer": False}  # fmt: skip
    s2 = e2 / e1 if ok(e2) else math.nan
    s3 = e3 / e1 if ok(e3) else math.nan
    entity = ok(s2) and ok(e3) and s2 >= ENTITY_KEEP - EPS and e3 <= ENTITY_A_MAX + EPS
    answer = ok(s2) and ok(s3) and s2 <= ANSWER_KEEP + EPS and s3 >= ANSWER_A_MIN - EPS
    key = "entity" if entity else "answer" if answer else "mixed"
    return {
        "label": LABELS[key],
        "key": key,
        "share2": s2,
        "share3": s3,
        "entity": bool(entity),
        "answer": bool(answer),
    }


def reader_numbers(rows: list[dict], reader: str, n_boot: int = X.N_BOOT, seed: int = X.BOOT_SEED) -> dict:
    """One reader: switch rate per arm, the three extra losses and the two shares (paired cluster-bootstrap CIs), the
    rule's label, X0's validity bar beside."""
    by = {(r["key"], r["arm"]): r for r in rows if r["reader"] == reader}
    keys = list(dict.fromkeys(r["key"] for r in rows if r["reader"] == reader and r["arm"] == "whole"))
    ent = {r["key"]: r["entity"] for r in rows}
    ents = [ent[k] for k in keys]
    sw = {a: [int(by[(k, a)]["sw"]) for k in keys] for a in ("none", *ARMS)}
    rr = X.resampled_rates(sw, ents, n_boot, seed)
    pt = {a: float(np.mean(v)) for a, v in sw.items()}
    e_pt, e_dr = {}, {}
    for k, (arm, rand) in PAIRS.items():
        e_pt[k] = excess(sw, arm, rand)
        e_dr[k] = X.dependence(rr["whole"], rr[arm]) - X.dependence(rr["whole"], rr[rand])
    with np.errstate(divide="ignore", invalid="ignore"):
        s2, s3 = e_dr[2] / e_dr[1], e_dr[3] / e_dr[1]
    r = rule(e_pt[1], e_pt[2], e_pt[3])
    return {"n": len(keys), "entities": len(set(ents)), "rate": {a: [pt[a], *X.interval(rr[a])] for a in sw},
            "hits": {a: int(sum(v)) for a, v in sw.items()},
            "extra": {str(k): [e_pt[k], *X.interval(e_dr[k])] for k in PAIRS},
            "share2": [r["share2"], *X.interval(s2)], "share3": [r["share3"], *X.interval(s3)],
            "valid": pt["whole"] >= X.VALID_S and sum(sw["whole"]) >= X.VALID_N, "label": r["label"], "key": r["key"],
            "clauses": {"entity": r["entity"], "answer": r["answer"]}}  # fmt: skip


def share_ci(values: list[int], ents: list[str], n_boot: int) -> list[float]:
    if not values:
        return [math.nan, math.nan, math.nan]
    rr = X.resampled_rates({"s": values}, ents, n_boot)["s"]
    return [float(np.mean(values)), *X.interval(rr)]


def readout_numbers(readout: list[dict], n_boot: int) -> dict:
    """Per source reader and prompt (O / S): the shares of items whose lens top-1 at the edited token is the own answer,
    the own bridge entity or neither; per reader's own answer separately; the other prompt's answer / bridge; the
    median rank of each reader's answer token (and among the digits, the share where it is the top digit)."""
    out: dict[str, Any] = {}
    for s in sorted({r["source"] for r in readout}):
        for v in ("org", "alt"):
            rs = [r for r in readout if r["source"] == s and r["variant"] == v]
            ents = [r["entity"] for r in rs]
            cell = {
                c: share_ci([int(r["class"] == c) for r in rs], ents, n_boot) for c in ("answer", "bridge", "neither")
            }
            readers = sorted({w for r in rs for w in r["answer_rank"]})
            cell |= {f"top1_is_{READER_NAME[w]}_answer": share_ci([int(w in r["own_answer_of"]) for r in rs], ents, n_boot)
                     for w in readers}  # fmt: skip
            cell["other_prompt_answer"] = share_ci([int(r["other_answer"]) for r in rs], ents, n_boot)
            cell["other_prompt_bridge"] = share_ci([int(r["other_bridge"]) for r in rs], ents, n_boot)
            cell["median_answer_rank"] = {
                READER_NAME[w]: float(np.median([r["answer_rank"][w] for r in rs])) for w in readers
            }
            dig = {w: [int(r["answer_digit_rank"][w] == 1) for r in rs if w in r["answer_digit_rank"]] for w in readers}
            cell["top_digit_is_answer"] = {READER_NAME[w]: share_ci(d, [r["entity"] for r in rs if w in r["answer_digit_rank"]], n_boot)
                                           for w, d in dig.items() if d}  # fmt: skip
            cell["n"] = len(rs)
            out[f"{READER_NAME.get(s, s)}'s prompt, {'O' if v == 'org' else 'S'}"] = cell
    return out


def atom_numbers(norms: list[dict]) -> dict:
    """Per source reader: |A| (tokens, rank) per item, and how many of Δ's 25 OMP atoms are answer atoms."""
    out = {}
    for s in sorted({n["source"] for n in norms}):
        ns = [n for n in norms if n["source"] == s]
        out[READER_NAME.get(s, s)] = {
            "A_tokens": size_summary([n["A_tokens"] for n in ns]), "A_rank": size_summary([n["A_rank"] for n in ns]),
            "A_letter_tokens": size_summary([n["A_letter_tokens"] for n in ns]),
            "answer_atoms_in_25": size_summary([n["n_answer_atoms_in_25"] for n in ns]),
            "items_with_an_answer_atom_in_25": sum(n["n_answer_atoms_in_25"] > 0 for n in ns),
            "share_median": {k: float(np.median([n[k] for n in ns])) for k in ns[0] if k.startswith("share_")}}  # fmt: skip
    return out


def model_result(set_name: str, target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    src = RESULTS / run
    if not (src / "manifest.json").exists():
        return {"set": set_name, "target": target, "run": run, "status": "pending", "why": "no manifest here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is not {target}'s"
    assert m["set"] == set_name, f"{run} is not a {set_name} run"
    gate = json.loads((src / "gate.json").read_text()) if (src / "gate.json").exists() else {}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    if not gate.get("tested") or not rows:
        return {"set": set_name, "target": target, "run": run, "status": "not tested", "gate": gate.get("gate"),
                "why": "the source gate failed, no items, or the run did not finish"}  # fmt: skip
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    agree = json.loads((src / "agreement.json").read_text()) if (src / "agreement.json").exists() else {}
    return {"set": set_name, "target": target, "run": run, "status": "tested", "layer": m["layer"],
            "source": m["source"], "gate": gate.get("gate"),
            "readers": {READER_NAME[w]: reader_numbers(rows, w, n_boot) for w in readers},
            "readout": readout_numbers(X.read_jsonl(src / "readout.jsonl"), n_boot),
            "atoms": atom_numbers(X.read_jsonl(src / "norms.jsonl")), "agreement": agree}  # fmt: skip


def fmt(v) -> str:
    return "-" if v is None or not ok(v[0]) else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


DECISIVE = {"z2": ("lookup", "recall"), "e1": ("recall",), "cue": ("lookup", "recall")}


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 51.12: is it the bridge or the answer that moves through the lens? (UNVERIFIED)", "",
             f"Batch 51, test 51.12 (jobs/c3/batch51.yaml addendum_4; {QUESTION}, Dan: {answer}). Cluster bootstrap over "
             f"the bridge entity ({n_boot}, seed {X.BOOT_SEED}), paired across arms.", "", f"Rule (fixed in advance): {RULE}",
             "", f"As computed: {AS_COMPUTED}", "",
             "| set | model | reader | n | e1 (no J++) | e2 (no J++, A kept) | e3 (no A) | e2/e1 | e3/e1 | label | decisive |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['set']} | {m['target']} | | {m['status']} ({m['why']}) | | | | | | | |")
            continue
        for w, r in m["readers"].items():
            lines.append(f"| {m['set']} | {m['target']} | {w} | {r['n']} | {fmt(r['extra']['1'])} | {fmt(r['extra']['2'])} "
                         f"| {fmt(r['extra']['3'])} | {fmt(r['share2'])} | {fmt(r['share3'])} | **{r['label']}** | "
                         f"{'yes' if w in DECISIVE[m['set']] else 'beside'} |")  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        lines += ["", f"## {m['set']} on {m['target']} ({m['run']}, L{m['layer']}, source {m['source']})", "",
                  f"Source gate: {m['gate']}.", "", "| arm | " + " | ".join(m["readers"]) + " |",
                  "|---|" + "---|" * len(m["readers"])]  # fmt: skip
        for a in ("none", *ARMS):
            lines.append(f"| {a} | " + " | ".join(fmt(r["rate"][a]) for r in m["readers"].values()) + " |")
        for w, r in m["readers"].items():
            lines.append(f"- {w}: X0's validity bar {r['valid']}; whole {r['hits']['whole']} of {r['n']}")
        lines += ["", "Answer directions and OMP atoms (per item):", ""]
        for s, a in m["atoms"].items():
            lines.append(f"- Δ from the {s}'s prompts: |A| tokens {a['A_tokens']}; rank {a['A_rank']}; letter tokens "
                         f"{a['A_letter_tokens']}; answer atoms among the 25: {a['answer_atoms_in_25']} "
                         f"({a['items_with_an_answer_atom_in_25']} items with at least one); median shares of ||Δ||^2 "
                         f"{ {k: round(v, 5) for k, v in a['share_median'].items()} }")  # fmt: skip
        lines += ["", "Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):", "",
                  "| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | "
                  "top digit = reader's answer |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for k, c in m["readout"].items():
            per = "; ".join(f"{kk[8:]}: {fmt(v)}" for kk, v in c.items() if kk.startswith("top1_is_"))
            dig = "; ".join(f"{w}: {fmt(v)}" for w, v in c["top_digit_is_answer"].items()) or "-"
            lines.append(f"| {k} | {c['n']} | {fmt(c['answer'])} | {fmt(c['bridge'])} | {fmt(c['neither'])} | {per} | "
                         f"{fmt(c['other_prompt_answer'])} | {dig} |")  # fmt: skip
        lines += ["", "Arm 1 against the stored run, item by item (agreement.json):", ""]
        for w, per in m["agreement"].items():
            el = per.get("extra_loss_arm1", {})
            lines.append(f"- {w}: " + "; ".join(f"{a} {v['agree_switch']}/{v['matched']} agree (rerun {v['rerun']}, "
                                                f"stored {v['stored']})" for a, v in per.items() if a != "extra_loss_arm1")
                         + f"; arm 1's extra loss rerun {el.get('rerun')} vs stored {el.get('stored')}")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + "."]
    return lines


def all_runs(sets: tuple[str, ...] = SETS) -> list[tuple[str, str, str]]:
    return [(s, t, r) for s in sets for t, r in RUNS[s].items()]


def stage_verdict(n_boot: int = X.N_BOOT, sets: tuple[str, ...] = SETS) -> Path:
    answer = unsealed()
    models = [model_result(s, t, r, n_boot) for s, t, r in all_runs(sets)]
    out = RESULTS / f"x51_12-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    per = {f"{m['set']}|{m['target']}|{w}": r["label"] for m in models if m["status"] == "tested"
           for w, r in m["readers"].items()}  # fmt: skip
    blob = {
        "dan": answer,
        "rule": RULE,
        "as_computed": AS_COMPUTED,
        "labels": LABELS,
        "models": models,
        "per_cell": per,
    }
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(set_name: str, target: str, run: str, decode, k_prompts: int = N_PROMPTS, k_rows: int = N_ROWS,
               seed: int = VIEW_SEED) -> list[str]:  # fmt: skip
    """The verify pack of one run: k_prompts items' prompts as read (O and S per reader, the edited token marked) and
    k_rows random rows per arm (seed 0)."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    rows = X.read_jsonl(src / "outcomes.jsonl")
    lines = [f"## {SET_TEXT[set_name]}: {target}, {run}", "",
             f"### {min(k_prompts, len(items))} rendered items of {len(items)} (seed {seed})", ""]  # fmt: skip
    for i in sorted(random.Random(seed).sample(range(len(items)), min(k_prompts, len(items)))):
        it = items[i]
        lines += [
            f"#### {it['key']}: {it['entity']} -> {it['cf_entity']}; A = {[decode([t]) for t in it['tokens']['A']]}",
            "",
        ]
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}**: O's answer {rd['answer']}, S's answer {rd['cf_answer']}", ""]
            for v in ("org", "alt"):
                lines += [f"{'O' if v == 'org' else 'S'}:", "", "```", mark(decode, rd["ids"][v] + rd["suffix"], rd["pos"]),
                          "```", ""]  # fmt: skip
    for a in ("none", *ARMS):
        mine = [r for r in rows if r["arm"] == a]
        pick = sorted(random.Random(seed).sample(range(len(mine)), min(k_rows, len(mine))))
        lines += [f"### {a}: {len(pick)} random rows of {len(mine)} (seed {seed})", "",
                  "| item | reader | top token | route | switch |", "|---|---|---|---|---|"]  # fmt: skip
        lines += [f"| {mine[j]['key']} | {READER_NAME[mine[j]['reader']]} | {decode([mine[j]['top']])!r} | "
                  f"{mine[j]['route']} | {mine[j]['sw']} |" for j in pick]  # fmt: skip
        lines.append("")
    return lines


def stage_view(sets: tuple[str, ...] = SETS, decode_for=None) -> Path:
    from scripts import x47_atoms as A

    unsealed()
    out = RESULTS / f"x51_12-view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 51.12 view (verify pack): prompts exactly as the model reads them; ⟦...⟧ the edited token, where each "
             "arm adds its vector at L. UNVERIFIED.", ""]  # fmt: skip
    for s, t, r in all_runs(sets):
        gate = RESULTS / r / "gate.json"
        if not gate.exists() or not json.loads(gate.read_text()).get("tested"):
            lines += [f"## {s} {t}: {r} not here or not tested", ""]
            continue
        lines += view_lines(s, t, r, (decode_for or A.default_decode)(t))
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--set", choices=SETS, help="plan / run: the set; verdict / view: one set (default all)")
    ap.add_argument("--name", help="run: the run name (results/x51_answer/<name>/)")
    ap.add_argument("--plan-dir", help="plan: the folder to write into (default a new plan-<UTC>/)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        assert a.set, "plan needs --set"
        stage_plan(a.set, a.plan_dir)
    elif a.stage == "run":
        assert a.name, "run needs --name"
        assert a.set, "run needs --set"
        stage_run(a.name, a.set)
    elif a.stage == "view":
        stage_view((a.set,) if a.set else SETS)
    else:
        stage_verdict(a.n_boot, (a.set,) if a.set else SETS)


if __name__ == "__main__":
    main()
