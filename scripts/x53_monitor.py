"""x53_monitor (batch 53, test 53.2, "the monitor test"; jobs/c3/batch53.yaml `brief:` 53.2, Dan 29 Oct 09:30; the
rule is fixed in advance by the brief; no prediction): what can a J-space readout decode, compared with the full state?

Brief, verbatim: "53.2 The monitor test: what a J-space readout can decode vs the full state. CPU on cached states
where they exist; forwards only where missing. Main test and the JSON varied scenes; 9B, 27B, Muse, Lightning.
Targets: (a) which item is the bridge; (b) the bridge item's locker slot (the address); (c) the lookup's answer digit;
(d) the recall's answer. Features at the bridge word and the last token, every 2nd layer: full residual; the J++ lens
subspace of dimension k (k = 25, 100); a random subspace of the same k; PCA top-k. Logistic probes, held-out entities,
same regularisation, 5 seeds. Rule: "J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every
layer while the full residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above
random; else in between. One figure: accuracy by layer, one panel per target, four feature lines."

Datasets (each reader's O and S prompts as the source run reads them, X0's chat read: the prompt with a digit's space
token appended):
  main  our main test: every item of the model's X0 run at L (x51_jread.select: 51.10's / 52 B's 200 items; S = the
        generator's cf, two people swap their picks); readers lookup (PP) and recall (PM).
  json  the varied scenes' JSON format (x0b_generalize's x0b_v2 set, format "json": tool outputs get_picks /
        get_lockers; every aligned scene, all levels and domains, no gate: a probe reads states, it does not need the
        reader right; each read's top token is recorded so the right-only rows can be read beside); S = x0b's alt (the
        asked pick becomes another person's pick).

Positions: B the bridge word (X0's position; the readers' prompts agree through it, so B is read on the lookup's
prompt and the recall's B is checked against it); T the last token (the appended space token) of each reader's prompt.
Layers: every second layer from L0 through n_layers - 2 (52 B's grid; those in the J++ lens's source layers).

Why a forward job although 52 B cached the main test's states (results/x52_answer_map/*_read_main/states.npz, fp16,
B / E / Q / T, the same grid): the J++ lens part of a state needs the lens maps and W_U, which are not on the Mac, and
the JSON scenes were cached at one layer and the bridge word only (x0b states.npz). The job re-runs the main test's
800 short forwards (minutes) so that one file holds every feature; the CPU stage checks its states against 52 B's.

Stage run (GPU, sealed: no probe, no label): per dataset one forward of each prompt (item x reader x O / S) recording
the block outputs at B and T at every cached layer, and the read's top token; then per layer, on the GPU, the J++ lens
part of every state: X0's signed OMP (exp04_brew_parts.signed_omp's steps) over the J++ letter-token atoms
(x0_necessity.dictionary("jpp"): unit J++ lens vectors of the letter tokens), the least-squares fit on the first k
atoms it picks, k = 25 (X0's K_MAIN) and 100 (OMP is greedy: the first 25 of the 100 are the k = 25 fit's atoms). Saved
fp16 per dataset (layer-major, gitignored): states_<set>_h.npy, states_<set>_jpp25.npy, states_<set>_jpp100.npy
[L, n, 2 (O / S), 3 (B, T lookup, T recall), d]; states_<set>_atoms.npy the 100 picked atoms' token ids (int32,
committed); cases_<set>.jsonl the items with their labels and reads (committed).

Stage probe (CPU, as runs arrive) and verdict (CPU): see the probe section below.

uv run python scripts/x53_monitor.py plan                                            # CPU, BJ_TARGET's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x53_monitor.py run --name qwen35_9b_x53_monitor   # GPU (sealed)
uv run python scripts/x53_monitor.py probe --name qwen35_9b_x53_monitor              # CPU: probes (cache/)
uv run python scripts/x53_monitor.py verdict                                         # CPU: rule, figure, x53_monitor-<UTC>/
"""

from __future__ import annotations

import argparse
import collections
import json
import re
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

EXP = "x53_monitor"
RESULTS = pins.RESULTS_DIR / EXP
CACHE = pins.CACHE_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"
NO_PREDICTION = "rule fixed in advance in jobs/c3/batch53.yaml (53.2); no prediction"
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
RUNS = {"qwen3.5-9b": "qwen35_9b_x53_monitor", "qwen3.6-27b": "x53_monitor_27b",
        "muse-glimmer-30b": "muse30_x53_monitor", "nemotron-3.5-lightning": "nem35l_x53_monitor"}  # fmt: skip
TAGS = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "nemotron-3.5-lightning": "lightning"}
NAMES = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B", "muse-glimmer-30b": "Muse-Glimmer-30B",
         "nemotron-3.5-lightning": "Nemotron-3.5-Lightning"}  # fmt: skip
D_MODEL = {"qwen3.5-9b": 4096, "qwen3.6-27b": 5120, "muse-glimmer-30b": 6656, "nemotron-3.5-lightning": 2688}  # plan
X52_READ = {"qwen3.5-9b": "qwen35_9b_x52_read_main", "qwen3.6-27b": "x52_read_main_27b",
            "muse-glimmer-30b": "muse30_x52_read_main", "nemotron-3.5-lightning": "nem35l_x52_read_main"}  # fmt: skip
SETS = ("main", "json")
SET_TEXT = {"main": "our main test (X0's scenes)", "json": "the varied scenes, JSON format (x0b_v2)",
            # 53.7 (batch 53, scripts/x53_7.py): the main test's items rendered as code / tool output; never in SETS
            "code": "the main test's scenes as Python code (53.7)", "tool": "the main test's scenes as tool output (53.7)"}  # fmt: skip
JSON_SET, JSON_FORMAT = "x0b_v2", "json"
VARIANTS = ("org", "alt")
POS = ("B", "T_lookup", "T_recall")
POS_TEXT = {"B": "the bridge word (X0's position; the readers' prompts agree through it: read on the lookup's prompt)",
            "T_lookup": "the lookup prompt's last token (the appended space token, before the answer)",
            "T_recall": "the recall prompt's last token (the appended space token, before the answer)"}  # fmt: skip
KS = (25, 100)
K_MAX = max(KS)
OMP_CHUNK = 256  # rows per OMP batch on the GPU
TOL_B = 0.02  # the recall's B state vs the lookup's: max relative difference reported (same prefix, kernels may differ)
RULE = ('"J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every layer while the full '
        'residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above random; else in '
        "between.")  # fmt: skip


# ---- labels and items (tokenizer only, CPU-testable) ---------------------------------------------------------------

LOCKER_RE = {
    "prose": re.compile(r"The locker of (?:the )?(.+?) is "),
    "json": re.compile(r'\{"item": "([^"]+)", "locker": '),
}


def locker_order(context: str, fmt: str) -> list[str]:
    """The things in the order of their locker statements in the context (prose: 'The locker of [the] X is ...';
    json: '{"item": "X", "locker": ...}'); asserted unique."""
    order = LOCKER_RE[fmt].findall(context)
    assert order, "no locker statement found"
    assert len(set(order)) == len(order), f"locker statements not found once each: {order}"
    return order


def slot_of(context: str, fmt: str, thing: str) -> tuple[int, int]:
    """(the thing's locker slot: its locker statement's ordinal among the locker statements, 0-based; their number)."""
    order = locker_order(context, fmt)
    assert thing in order, f"{thing!r} has no locker statement in {order}"
    return order.index(thing), len(order)


def labels(context: str, cf_context: str, fmt: str, bridge: str, cf_bridge: str, lookup: tuple[str, str],
           recall: tuple[str, str]) -> dict[str, dict]:  # fmt: skip
    """Per variant (O / S) the four targets: (a) the bridge item, (b) its locker slot, (c) the lookup's answer digit,
    (d) the recall's answer; S's locker statements are O's (asserted)."""
    assert locker_order(context, fmt) == locker_order(cf_context, fmt), "S moves a locker statement"
    out = {}
    for v, ctx, thing, i in (("org", context, bridge, 0), ("alt", cf_context, cf_bridge, 1)):
        slot, n_slots = slot_of(ctx, fmt, thing)
        out[v] = {"bridge": thing, "slot": slot, "n_slots": n_slots, "lookup": lookup[i], "recall": recall[i]}
    return out


def main_items(tok, target: str) -> tuple[list[dict], dict]:
    """main: 51.10's items (x51_jread.select: every item of the X0 run at L, positions P1 / P3 in O and S)."""
    from scripts import x51_jread as J

    items, counts = J.select(tok, target)
    out = []
    for it in items:
        readers = {}
        for w in X.READERS:
            rd, jp = it["readers"][w], it["jpos"][w]
            readers[w] = {"ids": rd["ids"], "suffix": it["space"], "question": rd["question"],
                          "pos": {v: {"B": jp["P1"][v], "T": jp["P3"][v]} for v in VARIANTS},
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")}}  # fmt: skip
        lab = labels(it["context"], it["cf_context"], "prose", it["entity"], it["cf_bridge"],
                     (readers[X.LOOKUP]["answer"], readers[X.LOOKUP]["cf_answer"]),
                     (readers[X.RECALL]["answer"], readers[X.RECALL]["cf_answer"]))  # fmt: skip
        out.append({"set": "main", "scene": it["scene"], "entity": it["entity"], "cf_entity": it["cf_bridge"],
                    "domain": it["domain"], "format": "prose", "lf": it["lf"], "context": it["context"],
                    "cf_context": it["cf_context"], "labels": lab, "readers": readers})  # fmt: skip
    return out, counts


def json_items(tok) -> tuple[list[dict], dict]:
    """json: every aligned JSON scene of x0b_v2 (x0b_generalize.build_cases: X0's checks, x0b's alt)."""
    from scripts import x0b_generalize as XB

    cases, counts = XB.build_cases(tok, JSON_SET)
    out = []
    for c in cases:
        if c["format"] != JSON_FORMAT:
            continue
        readers = {}
        for w in X.READERS:
            rd = c["readers"][w]
            pos = {v: {"B": c["pos"], "T": len(rd["ids"][v]) + len(c["space"]) - 1} for v in VARIANTS}
            readers[w] = {"ids": rd["ids"], "suffix": c["space"], "question": rd["question"], "pos": pos,
                          **{k: rd[k] for k in ("answer", "cf_answer", "tok_A", "tok_b")}}  # fmt: skip
        assert c["facts"]["x"] == c["bridge"], f"{c['scene']}: facts vs bridge"
        lab = labels(c["context"], c["cf_context"], JSON_FORMAT, c["bridge"], c["cf_bridge"],
                     (readers[X.LOOKUP]["answer"], readers[X.LOOKUP]["cf_answer"]),
                     (readers[X.RECALL]["answer"], readers[X.RECALL]["cf_answer"]))  # fmt: skip
        assert lab["org"]["n_slots"] == len(c["facts"]["locker"]), f"{c['scene']}: locker count"
        out.append({"set": "json", "scene": c["scene"], "entity": c["bridge"], "cf_entity": c["cf_bridge"],
                    "domain": c["domain"], "format": c["format"], "level": c["level"], "numbers": c["numbers"],
                    "order": c["order"], "context": c["context"], "cf_context": c["cf_context"], "labels": lab,
                    "readers": readers})  # fmt: skip
    kept = {"json_cases": len(out), "json_entities": len({it["entity"] for it in out}),
            "json_domains": dict(collections.Counter(it["domain"] for it in out)),
            "json_levels": dict(collections.Counter(str(it["level"]) for it in out)),
            "x0b_counts": {k: v for k, v in counts.items() if k != "cases_per_cell"}}  # fmt: skip
    return out, kept


def x53_7_items(tok, target: str, fmt: str) -> tuple[list[dict], dict]:
    """53.7's datasets (code, tool): the main test's items rendered in the format (scripts/x53_7.py main_items)."""
    from scripts import x53_7 as F

    return F.main_items(tok, target, fmt)


BUILD = {"main": lambda tok, target: main_items(tok, target), "json": lambda tok, target: json_items(tok),
         "code": lambda tok, target: x53_7_items(tok, target, "code"),
         "tool": lambda tok, target: x53_7_items(tok, target, "tool")}  # fmt: skip


def layers_for(n_layers: int) -> tuple[int, ...]:
    """Every second layer from L0 through n_layers - 2 (52 B's grid: the J++ lenses' last source layer)."""
    return tuple(range(0, n_layers - 1, 2))


def check_items(items: list[dict]) -> None:
    """Positions inside the read prompts; the readers' prompts identical through B (one B for both)."""
    for it in items:
        for v in VARIANTS:
            pp, pm = it["readers"][X.LOOKUP], it["readers"][X.RECALL]
            b = pp["pos"][v]["B"]
            assert pm["pos"][v]["B"] == b, f"{it['scene']} {v}: the readers' B differ"
            assert pp["ids"][v][: b + 1] == pm["ids"][v][: b + 1], f"{it['scene']} {v}: prompts differ through B"
            for rd in (pp, pm):
                assert rd["pos"][v]["T"] == len(rd["ids"][v]) + len(rd["suffix"]) - 1, f"{it['scene']}: T"
                assert 0 <= b < rd["pos"][v]["T"], f"{it['scene']}: B after T"


def stage_plan() -> Path:
    """Tokenizer only: both datasets' items, labels and counts for BJ_TARGET; the forwards and the file sizes."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    n_layers = pins.TARGETS[target]["n_layers"]
    layers = layers_for(n_layers)
    d = D_MODEL.get(target)
    blob: dict[str, Any] = {"target": target, "run": RUNS.get(target), "layers": list(layers)}
    for s in SETS:
        items, counts = BUILD[s](tok, target)
        check_items(items)
        blob[s] = {"items": len(items), "entities": len({it["entity"] for it in items}),
                   "forwards": len(items) * 2 * 2, "rows_per_position": 2 * len(items),
                   "slots": dict(collections.Counter(str(it["labels"][v]["slot"]) for it in items for v in VARIANTS)),
                   "lookup": dict(collections.Counter(it["labels"][v]["lookup"] for it in items for v in VARIANTS)),
                   "recall": dict(collections.Counter(it["labels"][v]["recall"] for it in items for v in VARIANTS)),
                   "bridges": len({it["labels"][v]["bridge"] for it in items for v in VARIANTS}),
                   "counts": counts}  # fmt: skip
        if d:
            blob[s]["mb_per_array_fp16"] = round(len(layers) * len(items) * 2 * len(POS) * d * 2 / 2**20)
    out = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    path = out / f"plan-{TAGS.get(target, target)}.json"
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "counts"}
                      for k, v in blob.items()}, indent=1))  # fmt: skip
    print("wrote", path)
    return path


# ---- GPU ----------------------------------------------------------------------------------------------------------


def forward_states(model, items: list[dict], layers: tuple[int, ...]) -> tuple[np.ndarray, list[dict]]:
    """One forward per item, reader and variant: the block outputs at B and T at the cached layers, fp16
    [L, n, 2 (O / S), 3 (B, T lookup, T recall), d]; per prompt the read's top token and B's reader gap."""
    import torch

    from bridge_jspace.utils import progress

    dev = model.device
    h: np.ndarray | None = None
    reads = []
    for i, it in enumerate(progress(items, "x53 forwards (item: 2 readers x O / S)")):
        rec_row: dict[str, Any] = {"scene": it["scene"]}
        for v, variant in enumerate(VARIANTS):
            b_states = {}
            for r, w in enumerate(X.READERS):
                rd = it["readers"][w]
                ids = torch.tensor([rd["ids"][variant] + rd["suffix"]], device=dev)
                logits, rec = model.run(ids, record=layers)
                if h is None:
                    d = rec[layers[0]].shape[-1]
                    h = np.zeros((len(layers), len(items), 2, len(POS), d), dtype=np.float16)
                p = rd["pos"][variant]
                b_states[w] = torch.stack([rec[la][p["B"]] for la in layers])
                t_states = torch.stack([rec[la][p["T"]] for la in layers])
                if w == X.LOOKUP:
                    h[:, i, v, 0] = b_states[w].cpu().numpy().astype(np.float16)
                h[:, i, v, 1 + r] = t_states.cpu().numpy().astype(np.float16)
                top = int(logits.argmax())
                want = rd["tok_A"] if variant == "org" else rd["tok_b"]
                rec_row[f"{w}_{variant}"] = {"top": top, "right": top == want}
                del rec
            gap = (b_states[X.RECALL] - b_states[X.LOOKUP]).norm(dim=-1) / b_states[X.LOOKUP].norm(dim=-1)
            rec_row[f"b_gap_{variant}"] = float(gap.max())
        reads.append(rec_row)
    assert h is not None, "no items"
    assert np.isfinite(h).all(), "fp16 overflow in the cached states"
    return h, reads


def omp_parts(dic, x, ks: tuple[int, ...]):
    """X0's signed OMP (exp04_brew_parts.signed_omp, step for step) run to max(ks) atoms on the rows of x [m, d]: the
    least-squares fit on the first k chosen atoms for each k in ks ({k: [m, d] fp32}) and the chosen atoms [m, max]."""
    import torch

    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    parts = {}
    for step in range(1, max(ks) + 1):
        scores = ((x - approx) @ dic.T).abs()  # [m, n]
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dic[chosen].double()  # [m, s, d]
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + 1e-8 * eye, rhs)  # [m, s]
        approx = (coefs.unsqueeze(1) @ atoms).squeeze(1).float()
        if step in ks:
            parts[step] = approx.clone()
        del scores, atoms, gram, rhs
    return parts, chosen


def lens_parts(model, lens, h: np.ndarray, layers: tuple[int, ...]) -> tuple[dict[int, np.ndarray], np.ndarray]:
    """Per layer the J++ part of every cached state at k in KS (fp16, h's shape) and the K_MAX atoms' token ids."""
    import torch

    from bridge_jspace.utils import progress

    letters = model.letter_token_ids()
    shape = h.shape  # [L, n, 2, 3, d]
    parts = {k: np.zeros(shape, dtype=np.float16) for k in KS}
    atoms = np.zeros((*shape[:-1], K_MAX), dtype=np.int32)
    for li, la in enumerate(progress(layers, "x53 J++ parts (layer)")):
        dic = X.dictionary("jpp", la, model, lens, letters)  # unit J++ vectors of the letter tokens [n_letters, d]
        flat = h[li].reshape(-1, shape[-1])
        out = {k: np.zeros(flat.shape, dtype=np.float16) for k in KS}
        ids = np.zeros((flat.shape[0], K_MAX), dtype=np.int32)
        for s in range(0, flat.shape[0], OMP_CHUNK):
            x = torch.from_numpy(flat[s : s + OMP_CHUNK].astype(np.float32)).to(dic.device)
            got, chosen = omp_parts(dic, x, KS)
            for k in KS:
                out[k][s : s + OMP_CHUNK] = got[k].cpu().numpy().astype(np.float16)
            ids[s : s + OMP_CHUNK] = letters.to(chosen.device)[chosen].cpu().numpy().astype(np.int32)
            del x, got, chosen
        for k in KS:
            parts[k][li] = out[k].reshape(shape[1:])
        atoms[li] = ids.reshape((*shape[1:-1], K_MAX))
        del dic
        lens._J_gpu.clear()  # one layer's J at a time (the 27B / Muse keep 32 / 26 maps otherwise)
        torch.cuda.empty_cache()
    for k in KS:
        assert np.isfinite(parts[k]).all(), f"fp16 overflow in the J++ parts (k = {k})"
    return parts, atoms


def manifest(name: str, target: str, extra: dict) -> dict:
    from bridge_jspace.utils import git_state

    return {"exp": EXP, "run": name, "spec": f"jobs/c3/batch53.yaml (53.2); jobs/c3/x53_monitor_{TAGS[target]}.yaml",
            "prediction": NO_PREDICTION, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(),
            "sets": SET_TEXT, "positions": POS_TEXT, "ks": list(KS), "rule": RULE,
            "jpp_part": "X0's signed OMP over the J++ letter-token atoms (x0_necessity.dictionary('jpp')), the "
                        "least-squares fit on the first k chosen atoms, applied to the state itself",
            "storage": "states_<set>_{h,jpp25,jpp100}.npy fp16 [L, n, O/S, B/T lookup/T recall, d] (gitignored); "
                       "states_<set>_atoms.npy int32 token ids of the 100 chosen atoms (committed)",
            **extra}  # fmt: skip


def stage_run(name: str, sets_run: tuple[str, ...] = SETS, model=None, extra: dict | None = None) -> Path:
    """sets_run, model, extra (53.7, scripts/x53_7.py): the datasets to record (default SETS, as before), an already
    loaded model, and more manifest keys (53.7's gate)."""
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "x53 reads the sources' chat prompts: run with BJ_FORMAT unset"
    assert set(sets_run) <= set(BUILD), f"datasets {sets_run}: of {tuple(BUILD)}"
    target = pins.TARGET
    assert target in MODELS, f"x53_monitor runs on {MODELS}, not {target}"
    n_layers = pins.TARGETS[target]["n_layers"]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, pins.DATA_DIR / "tasks_v2" / JSON_SET / "items.jsonl"]
    m = manifest(name, target, {"inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs},
                                "layers_candidate": list(layers_for(n_layers)), "n_layers": n_layers,
                                **({"sets_run": list(sets_run)} if sets_run != SETS else {}), **(extra or {})})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = model if model is not None else load_model()
    lens = JLens(model, "jpp")
    layers = tuple(la for la in layers_for(n_layers) if la in lens.source_layers)
    assert layers, "the J++ lens has no map at any candidate layer"
    sets: dict[str, Any] = {}
    for s in sets_run:
        items, counts = BUILD[s](model.tokenizer, target)
        check_items(items)
        assert items, f"{s}: no items"
        with torch.no_grad():
            h, reads = forward_states(model, items, layers)
            parts, atoms = lens_parts(model, lens, h, layers)
        np.save(out / f"states_{s}_h.npy", h)
        for k in KS:
            np.save(out / f"states_{s}_jpp{k}.npy", parts[k])
        np.save(out / f"states_{s}_atoms.npy", atoms)
        X.write_jsonl(out / f"cases_{s}.jsonl", [{**it, "read": rd} for it, rd in zip(items, reads, strict=True)])
        gaps = [max(rd["b_gap_org"], rd["b_gap_alt"]) for rd in reads]
        sets[s] = {"items": len(items), "entities": len({it["entity"] for it in items}), "counts": counts,
                   "b_gap_max": float(max(gaps)), "b_gap_over_tol": int(sum(g > TOL_B for g in gaps))}  # fmt: skip
        print(f"{s}: {len(items)} items, {len(layers)} layers, B reader gap max {max(gaps):.2e}", flush=True)
        del h, parts, atoms
    m.update({"layers": list(layers), "sets_done": sets, "hub_kernels": loaded_hub_kernels(),
              "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out} (no probe, no label: the CPU stages read it)", flush=True)
    return out


# ---- CPU: probes -----------------------------------------------------------------------------------------------------
# Per model, dataset, layer and row set (B; T lookup for (a)-(c); T recall for (d)): features full / J++_k / random_k /
# PCA_k; multinomial logistic probes (sklearn's objective, C = 1.0 for all, standardised on the training rows), 5 seeds
# x 5-fold CV (as the specs' decision rule writes it), grouped by the row's bridge entity for (b) and (c) and by scene
# for (a) and (d); per row in how many seeds its out-of-fold prediction is right (cache/x53_monitor/<run>/<set>.npz).

TARGETS = ("a", "b", "c", "d")
TARGET_KEY = {"a": "bridge", "b": "slot", "c": "lookup", "d": "recall"}
TARGET_TEXT = {"a": "(a) which item is the bridge", "b": "(b) the bridge item's locker slot (the address)",
               "c": "(c) the lookup's answer digit", "d": "(d) the recall's answer"}  # fmt: skip
TARGET_SHORT = {
    "a": "(a) which item",
    "b": "(b) its locker slot",
    "c": "(c) lookup's digit",
    "d": "(d) recall's answer",
}
GROUP_BY = {"a": "scene", "b": "entity", "c": "entity", "d": "scene"}
GROUP_TEXT = {"entity": "held-out entities (folds grouped by the row's bridge entity)",
              "scene": "held-out scenes (a held-out entity is an unseen class here; x0_probe's precedent): folds "
                       "grouped by scene, a scene's O and S rows together"}  # fmt: skip
PROBE_POS = ("B", "T")
PROBE_POS_TEXT = {"B": "the bridge word", "T": "the last token (lookup's prompt for (a)-(c), recall's for (d))"}
ROW_OF = {**{("B", t): 0 for t in TARGETS}, ("T", "a"): 1, ("T", "b"): 1, ("T", "c"): 1, ("T", "d"): 2}
FEATURES = ("full", *(f"jpp{k}" for k in KS), *(f"rand{k}" for k in KS), *(f"pca{k}" for k in KS))
FEATURE_TEXT = {"full": "the full residual (the block output)",
                **{f"jpp{k}": f"the J++ lens part, k = {k} (X0's signed OMP of the state over the J++ letter atoms)"
                   for k in KS},
                **{f"rand{k}": f"a random {k}-dimensional subspace (Haar, seed 888 + layer + 1000 x probe seed)"
                   for k in KS},
                **{f"pca{k}": f"PCA top-{k} of the training rows" for k in KS},
                "chance": "the training folds' majority class"}  # fmt: skip
# Dan 11:25 (jobs/c3/batch53.yaml critic_1125, before scoring): two more arms beside the current ones, each in its own
# probe pass (same folds, same probe), and the same rule with J++ replaced by the fixed subspace:
#   fix_k   a fixed J++ subspace per fold: the span of the k J++ letter atoms most frequent among the training rows'
#           first-k OMP atoms (ties: the smaller token id), applied unchanged to the held-out rows (k = 25, 100)
#   erand_k an energy-matched random subspace: its dimension r = round(the J++_k part's median share of the state's
#           squared norm, over all rows of that layer and row set (label-free), x d), so a Haar subspace keeps that
#           share in expectation (E ||P h||^2 = r / d ||h||^2); the first r columns of the same seeded frame as random_k.
#           Rescaling a k-dimensional random part instead would change nothing: the probes standardise each feature.
PASSES = {"base": (*FEATURES, "chance"), "erand": tuple(f"erand{k}" for k in KS), "fixed": tuple(f"fix{k}" for k in KS)}
FEATURE_TEXT.update(
    {
        **{
            f"fix{k}": f"a fixed J++ subspace: the span of the {k} J++ atoms most frequent on the training folds"
            for k in KS
        },
        **{
            f"erand{k}": f"a random subspace of the J++_{k} part's median energy share (dimension = share x d)"
            for k in KS
        },
    }
)
C_REG, N_SEEDS, N_FOLDS = 1.0, 5, 5
RAND_SEED_STEP = 1000
LBFGS_MAXITER = 1000
LBFGS_GTOL, LBFGS_FTOL = 1e-3, 1e-7  # dev check (9B L12, one fold): same objective to 3 decimals and the same
# held-out accuracy as scipy's defaults (1e-5 / 2.2e-9) on every target and feature, 1.3-3x fewer iterations
BLIND_GAP, FULL_MIN, CARRY_MIN, CARRY_GAP = 0.10, 0.8, 0.8, 0.3
EPS = 1e-9
WORKERS = 8
LABELS = ("J-space blind to X", "J-space carries X", "in between")


def row_table(items: list[dict]) -> dict[str, np.ndarray]:
    """Rows in (item, O / S) order (row 2 i + v): the row's bridge entity, its scene and the four targets' labels."""
    ent, scene, y = [], [], {t: [] for t in TARGETS}
    for it in items:
        for v in VARIANTS:
            lab = it["labels"][v]
            ent.append(lab["bridge"])
            scene.append(it["scene"])
            for t in TARGETS:
                y[t].append(str(lab[TARGET_KEY[t]]))
    return {"entity": np.array(ent), "scene": np.array(scene), **{f"y_{t}": np.array(y[t]) for t in TARGETS}}


def fold_ids(groups: np.ndarray, seed: int, k: int = N_FOLDS) -> np.ndarray:
    """Each group to one of k folds (a seeded random order of the groups, dealt round-robin); per row its fold."""
    uniq = np.unique(groups)
    order = uniq[np.random.default_rng(seed).permutation(len(uniq))]
    fold_of = {g: j % k for j, g in enumerate(order)}
    return np.array([fold_of[g] for g in groups])


def random_frame(d: int, layer: int, seed: int, k: int) -> np.ndarray:
    """The first k columns of statement_positions.random_basis's Haar basis (QR of a d x d Gaussian, signs fixed), seed
    888 + layer + 1000 x seed (seed 0: X0's random basis): QR's first k columns depend on the first k columns only."""
    import torch

    g = torch.Generator().manual_seed(X.SUBSPACE_SEED + layer + RAND_SEED_STEP * seed)
    a = torch.randn(d, d, generator=g)[:, :k].double()
    q, r = torch.linalg.qr(a)
    return (q * torch.sign(torch.diagonal(r))).numpy()


def standardize(tr: np.ndarray, te: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """sklearn's StandardScaler fit on the training rows (a constant column keeps scale 1)."""
    mu, sd = tr.mean(0), tr.std(0)
    sd = np.where(sd > 1e-12, sd, 1.0)
    return (tr - mu) / sd, (te - mu) / sd


def span_coords(tr: np.ndarray, te: np.ndarray, tol: float = 1e-10) -> tuple[np.ndarray, np.ndarray]:
    """The rows in the training rows' span (Z = U S V^T: Z V = U S, Z_te V = Z_te Z^T U / S). An L2-penalised linear
    model's weights lie in that span and ||V a|| = ||a||, so the fit there is the fit in the full space."""
    w, u = np.linalg.eigh(tr @ tr.T)
    keep = w > tol * max(float(w.max()), 1e-300)
    u, s = u[:, keep], np.sqrt(w[keep])
    return u * s, (te @ tr.T) @ (u / s)


def pca_coords(tr: np.ndarray, te: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    """The rows' projections on the training rows' top-k principal directions (centred on the training rows)."""
    mu = tr.mean(0)
    a, b = tr - mu, te - mu
    w, u = np.linalg.eigh(a @ a.T)
    order = np.argsort(w)[::-1][:k]
    w, u = w[order], u[:, order]
    keep = w > 1e-10 * max(float(w.max()), 1e-300)
    u, s = u[:, keep], np.sqrt(w[keep])
    return u * s, (b @ a.T) @ (u / s)


def logistic(xtr: np.ndarray, ytr: np.ndarray, xte: np.ndarray, c: float = C_REG) -> np.ndarray:
    """Multinomial logistic regression, sklearn's objective: 0.5 ||W||^2 + c x the summed log-loss, the intercept not
    penalised; scipy L-BFGS. The predicted labels of xte (a class absent from training is never predicted)."""
    from scipy.optimize import minimize
    from scipy.special import logsumexp

    classes, y = np.unique(ytr, return_inverse=True)
    if len(classes) == 1:
        return np.full(len(xte), classes[0])
    n, f = xtr.shape
    k = len(classes)
    onehot = np.eye(k)[y]

    def fg(theta: np.ndarray) -> tuple[float, np.ndarray]:
        w, b = theta[: f * k].reshape(f, k), theta[f * k :]
        z = xtr @ w + b
        lse = logsumexp(z, axis=1)
        loss = float((lse - z[np.arange(n), y]).sum())
        g = np.exp(z - lse[:, None]) - onehot
        grad = np.concatenate([(c * (xtr.T @ g) + w).ravel(), c * g.sum(0)])
        return c * loss + 0.5 * float((w * w).sum()), grad

    res = minimize(fg, np.zeros(f * k + k), jac=True, method="L-BFGS-B",
                   options={"maxiter": LBFGS_MAXITER, "gtol": LBFGS_GTOL, "ftol": LBFGS_FTOL})  # fmt: skip
    w, b = res.x[: f * k].reshape(f, k), res.x[f * k :]
    return classes[np.argmax(xte @ w + b, axis=1)]


def fixed_atoms(atoms_rows: np.ndarray, k: int) -> np.ndarray:
    """The k token ids most frequent among the rows' first k J++ atoms (atoms_rows [n, K_MAX], OMP order; ties: the
    smaller id): the fixed J++ subspace's atoms for those (training) rows."""
    ids, cnt = np.unique(atoms_rows[:, :k], return_counts=True)
    return ids[np.lexsort((ids, -cnt))][:k]


def erand_dims(jpp_share: dict[int, float], d: int) -> dict[int, int]:
    """The energy-matched random subspace's dimension per k: round(J++_k's median share x d), at least 1, at most d."""
    return {k: int(min(d, max(1, round(jpp_share[k] * d)))) for k in KS}


def fold_features(pass_: str, ctx: dict, s: int, tr: np.ndarray, te: np.ndarray) -> dict:
    """One pass's features for one fold, (train, test) each: full and J++_k standardised in the training span;
    random_k, PCA_k and fix_k (k-dimensional) standardised; erand_k (r-dimensional) standardised in the training span."""
    mats = ctx["mats"]
    feats = {}
    if pass_ == "base":
        feats["full"] = span_coords(*standardize(mats["h"][tr], mats["h"][te]))
        for k in KS:
            feats[f"jpp{k}"] = span_coords(*standardize(mats[f"jpp{k}"][tr], mats[f"jpp{k}"][te]))
        rand_all = ctx["proj"][s]
        for k in KS:
            feats[f"rand{k}"] = standardize(rand_all[tr, :k], rand_all[te, :k])
        for k in KS:
            feats[f"pca{k}"] = standardize(*pca_coords(mats["h"][tr], mats["h"][te], k))
    elif pass_ == "erand":
        rand_all = ctx["proj"][s]
        for k in KS:
            r = ctx["erand_dims"][k]
            feats[f"erand{k}"] = span_coords(*standardize(rand_all[tr, :r], rand_all[te, :r]))
    else:
        assert pass_ == "fixed", pass_
        for k in KS:
            ids = fixed_atoms(ctx["atoms"][tr], k)
            rows = [ctx["atom_row"][int(t)] for t in ids]  # KeyError: an atom the box did not save (stage atom-ids)
            q, _ = np.linalg.qr(ctx["atom_vec"][rows].astype(np.float64).T)  # [d, k] orthonormal basis of their span
            proj = mats["h"] @ q
            feats[f"fix{k}"] = standardize(proj[tr], proj[te])
    return feats


def probe_matrix(pass_: str, ctx: dict, rows: dict[str, np.ndarray], cells: list[tuple[str, str]]) -> dict:
    """One pass on one row set at one layer: per cell (position, target) and feature (and, in the base pass, chance),
    per row [2, n_rows]: in how many seeds its out-of-fold prediction is right, and in how many seeds it was held out
    (5-fold per seed: every seed)."""
    n = len(rows["entity"])
    out = {}
    for grouping in sorted({GROUP_BY[t] for _, t in cells}):
        mine = [(p, t) for p, t in cells if GROUP_BY[t] == grouping]
        groups = rows[grouping]
        right = {(p, t, f): np.zeros(n, np.float32) for p, t in mine for f in PASSES[pass_]}
        tested = np.zeros(n, np.float32)
        for s in range(N_SEEDS):
            folds = fold_ids(groups, s)
            for f in range(N_FOLDS):
                te = folds == f
                tr = ~te
                tested[te] += 1
                feats = fold_features(pass_, ctx, s, tr, te)
                for p, t in mine:
                    y = rows[f"y_{t}"]
                    for name, (xtr, xte) in feats.items():
                        right[(p, t, name)][te] += logistic(xtr, y[tr], xte) == y[te]
                    if pass_ == "base":
                        vals, cnt = np.unique(y[tr], return_counts=True)
                        right[(p, t, "chance")][te] += y[te] == vals[np.argmax(cnt)]
        out.update({"|".join(key): np.stack([a, tested]) for key, a in right.items()})
    return out


def probe_layer(job: dict) -> dict:
    """One layer of one run and dataset (a worker): one pass's probes on every row set."""
    import torch

    torch.set_num_threads(1)  # the random frames' QR: one thread per worker (8 workers x all cores stalls the Mac)
    t0 = time.time()
    li, la, rows, pass_ = job["li"], job["layer"], job["rows"], job["pass"]
    arrs = {name: np.load(path, mmap_mode="r") for name, path in job["paths"].items()}
    n = len(rows["entity"])
    d = arrs["h"].shape[-1]
    fixed = None
    if pass_ == "fixed":
        z = np.load(job["fixed_atoms"])
        fixed = {"ids": z[f"ids_L{la}"], "vec": z[f"vec_L{la}"]}
    out: dict[str, np.ndarray] = {}
    for m in sorted(set(ROW_OF.values())):
        cells = [(p, t) for p in PROBE_POS for t in TARGETS if ROW_OF[(p, t)] == m]
        mats = {name: np.asarray(a[li][:, :, m], dtype=np.float64).reshape(n, d)
                for name, a in arrs.items() if name != "atoms"}  # fmt: skip
        sq = (mats["h"] ** 2).sum(1) + 1e-30
        share = {k: (mats[f"jpp{k}"] ** 2).sum(1) / sq for k in KS}
        ctx: dict[str, Any] = {"mats": mats}
        if pass_ == "base":
            ctx["proj"] = {s: mats["h"] @ random_frame(d, la, s, K_MAX) for s in range(N_SEEDS)}
        elif pass_ == "erand":
            ctx["erand_dims"] = erand_dims({k: float(np.median(share[k])) for k in KS}, d)
            r_max = max(ctx["erand_dims"].values())
            ctx["proj"] = {s: mats["h"] @ random_frame(d, la, s, r_max) for s in range(N_SEEDS)}
        else:
            assert fixed is not None
            ctx["atoms"] = np.asarray(arrs["atoms"][li][:, :, m]).reshape(n, K_MAX)
            ctx["atom_row"] = {int(t): i for i, t in enumerate(fixed["ids"])}
            ctx["atom_vec"] = fixed["vec"]
        out.update(probe_matrix(pass_, ctx, rows, cells))
        ones = np.ones(n, np.float32)
        if pass_ == "base":  # beside: each feature's share of the state's squared norm per row (probe seed 0)
            for k in KS:
                out[f"{POS[m]}|share|jpp{k}"] = np.stack([share[k], ones]).astype(np.float32)
                rand = (ctx["proj"][0][:, :k] ** 2).sum(1) / sq
                out[f"{POS[m]}|share|rand{k}"] = np.stack([rand, ones]).astype(np.float32)
        elif pass_ == "erand":
            for k in KS:
                r = ctx["erand_dims"][k]
                rand = (ctx["proj"][0][:, :r] ** 2).sum(1) / sq
                out[f"{POS[m]}|share|erand{k}"] = np.stack([rand, ones]).astype(np.float32)
                out[f"{POS[m]}|dim|erand{k}"] = np.stack([np.full(n, r, np.float32), ones])
    return {"li": li, "layer": la, "right": out, "seconds": time.time() - t0}


def state_paths(run_dir: Path, s: str) -> dict[str, Path]:
    return {"h": run_dir / f"states_{s}_h.npy", **{f"jpp{k}": run_dir / f"states_{s}_jpp{k}.npy" for k in KS},
            "atoms": run_dir / f"states_{s}_atoms.npy"}  # fmt: skip


def cache_file(name: str, s: str, pass_: str) -> Path:
    return CACHE / name / (f"{s}.npz" if pass_ == "base" else f"{s}_{pass_}.npz")


def stage_probe(name: str, states_root: Path, sets: tuple[str, ...] = SETS, workers: int = WORKERS,
                pass_: str = "base") -> list[Path]:  # fmt: skip
    """CPU: one pass of the probes of one run (per dataset, every layer in parallel) into cache/x53_monitor/<run>/."""
    import os
    from concurrent.futures import ProcessPoolExecutor, as_completed

    from bridge_jspace.utils import progress

    for var in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[var] = "1"  # one BLAS thread per worker (inherited by the spawned workers)
    run_dir = states_root / name
    m = json.loads((run_dir / "manifest.json").read_text())
    layers = m["layers"]
    written = []
    for s in sets:
        items = X.read_jsonl(run_dir / f"cases_{s}.jsonl")
        rows = row_table(items)
        paths = {k: str(p) for k, p in state_paths(run_dir, s).items()}
        h = np.load(paths["h"], mmap_mode="r")
        assert h.shape[:4] == (len(layers), len(items), 2, len(POS)), f"{name} {s}: states {h.shape} vs the cases"
        fixed = None
        if pass_ == "fixed":
            path = states_root / atoms_run(name) / f"fixed_atoms_{s}.npz"
            assert path.exists(), f"{path}: the box's atoms stage (spec x53_monitor_atoms_*) has not been pulled"
            fixed = str(path)
        jobs = [{"li": li, "layer": la, "rows": rows, "paths": paths, "pass": pass_, "fixed_atoms": fixed}
                for li, la in enumerate(layers)]  # fmt: skip
        got: dict[int, dict] = {}
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(probe_layer, j) for j in jobs]
            for fut in progress(as_completed(futs), f"x53 probes {name} {s} {pass_} (layer)", total=len(futs)):
                r = fut.result()
                got[r["li"]] = r
        keys = sorted(got[0]["right"])
        out = cache_file(name, s, pass_)
        out.parent.mkdir(parents=True, exist_ok=True)
        np.savez(out, layers=np.array(layers), keys=np.array(keys),
                 right=np.stack([np.stack([got[li]["right"][k] for li in range(len(layers))]) for k in keys]),
                 entity=rows["entity"], scene=rows["scene"],
                 seconds=np.array([got[li]["seconds"] for li in range(len(layers))]))  # fmt: skip
        print(f"wrote {out}: {len(keys)} cells x {len(layers)} layers x {len(rows['entity'])} rows", flush=True)
        written.append(out)
    return written


def atoms_run(name: str) -> str:
    """The atoms stage's run (the fixed J++ subspaces' atom vectors) for a forward run."""
    return f"{name}_atoms"


def needed_atom_ids(atoms: np.ndarray, rows: dict[str, np.ndarray]) -> list[int]:
    """At one layer (atoms [n, 2, 3, K_MAX]): every token id that some fold's fixed J++ subspace uses (any row set,
    grouping, seed, fold and k), i.e. exactly the atoms the fixed pass will look up."""
    n2 = len(rows["entity"])
    need: set[int] = set()
    for m in sorted(set(ROW_OF.values())):
        a = np.asarray(atoms[:, :, m]).reshape(n2, K_MAX)
        for grouping in sorted({GROUP_BY[t] for (p, t), mm in ROW_OF.items() if mm == m}):
            for s in range(N_SEEDS):
                folds = fold_ids(rows[grouping], s)
                for f in range(N_FOLDS):
                    for k in KS:
                        need.update(int(t) for t in fixed_atoms(a[folds != f], k))
    return sorted(need)


def stage_atom_ids(name: str, states_root: Path) -> Path:
    """CPU: the token ids the fixed J++ subspaces need, per dataset and layer (the box computes their vectors):
    results/x53_monitor/<run>/fixed_atom_ids.json."""
    run_dir = states_root / name
    layers = json.loads((run_dir / "manifest.json").read_text())["layers"]
    blob: dict[str, Any] = {"run": name, "what": "per dataset and layer, every J++ atom (token id) some training fold's "
                            "fixed J++ subspace uses (k = 25, 100; any row set, grouping, seed, fold)", "sets": {}}  # fmt: skip
    for s in SETS:
        rows = row_table(X.read_jsonl(run_dir / f"cases_{s}.jsonl"))
        atoms = np.load(run_dir / f"states_{s}_atoms.npy", mmap_mode="r")
        blob["sets"][s] = {str(la): needed_atom_ids(np.asarray(atoms[li]), rows) for li, la in enumerate(layers)}
        sizes = [len(v) for v in blob["sets"][s].values()]
        print(f"{name} {s}: {min(sizes)}-{max(sizes)} atoms per layer", flush=True)
    out = RESULTS / name / "fixed_atom_ids.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(blob) + "\n")
    print("wrote", out)
    return out


def stage_atoms(name: str, source: str) -> Path:
    """GPU: the unit J++ lens vectors (x0_necessity.dictionary('jpp')'s rows) of the atoms in
    results/x53_monitor/<source>/fixed_atom_ids.json, per dataset and layer, into results/x53_monitor/<name>/
    fixed_atoms_<set>.npz (name = <source>_atoms; ids_L<l> int64, vec_L<l> fp16; gitignored)."""
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state

    pins.check_run_name(name)
    target = pins.TARGET
    assert target in MODELS, f"x53_monitor runs on {MODELS}, not {target}"
    assert source == RUNS[target], f"{source}: not {target}'s x53 run ({RUNS[target]})"
    assert name == atoms_run(source), f"the atoms run is {atoms_run(source)}, not {name}"
    src = RESULTS / source / "fixed_atom_ids.json"
    need = json.loads(src.read_text())
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "stage": "atoms", "source": source, "prediction": NO_PREDICTION,
         "spec": f"jobs/c3/batch53.yaml (53.2, critic_1125); jobs/c3/x53_monitor_atoms_{TAGS[target]}.yaml",
         "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
         "switches": switches(), "code": git_state(), "lens": X.lens_record(),
         "inputs": {str(src.relative_to(pins.REPO_ROOT)): X.sha256_of(src)},
         "what": "unit J++ lens vectors of the fixed J++ subspaces' atoms (lens.vectors, as x0_necessity.dictionary)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    model = load_model()
    lens = JLens(model, "jpp")
    letters = set(model.letter_token_ids().tolist())
    with torch.no_grad():
        for s, per_layer in need["sets"].items():
            blob = {}
            for la, ids in per_layer.items():
                assert set(ids) <= letters, f"{s} L{la}: an atom that is not a letter token"
                vec = lens.vectors(int(la), torch.tensor(ids, device=model.device))
                blob[f"ids_L{la}"] = np.array(ids, dtype=np.int64)
                blob[f"vec_L{la}"] = vec.cpu().numpy().astype(np.float16)
            np.savez(out / f"fixed_atoms_{s}.npz", **blob)
            print(f"{s}: {len(per_layer)} layers, {sum(len(v) for v in per_layer.values())} atom vectors", flush=True)
            lens._J_gpu.clear()
            torch.cuda.empty_cache()
    m["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out, flush=True)
    return out


# ---- CPU: the rule, the figure, the verdict ------------------------------------------------------------------------


def rule_label(full: np.ndarray, jpp: np.ndarray, rand: np.ndarray) -> dict:
    """53.2's rule on per-layer point estimates (EPS at the bars): blind iff |J++ - random| <= 0.10 at every layer and
    full >= 0.8 at some layer; carries iff J++ >= 0.8 and J++ - random >= 0.3 at some layer; else in between."""
    gap = jpp - rand
    blind = bool(np.all(np.abs(gap) <= BLIND_GAP + EPS) and np.any(full >= FULL_MIN - EPS))
    carry_at = np.flatnonzero((jpp >= CARRY_MIN - EPS) & (gap >= CARRY_GAP - EPS))
    carries = bool(len(carry_at))
    assert not (blind and carries)
    label = LABELS[0] if blind else LABELS[1] if carries else LABELS[2]
    return {"label": label, "full_max": float(full.max()), "jpp_max": float(jpp.max()),
            "gap_max": float(gap.max()), "gap_abs_max": float(np.abs(gap).max()),
            "carry_layers_idx": [int(i) for i in carry_at], "full_reaches_0.8": bool(np.any(full >= FULL_MIN - EPS))}  # fmt: skip


def cluster_ci(num: np.ndarray, den: np.ndarray, clusters: np.ndarray, n_boot: int = X.N_BOOT,
               seed: int = X.BOOT_SEED) -> np.ndarray:  # fmt: skip
    """95% percentile CIs of sum(num) / sum(den) for each column of num, den [n_rows, m] (rows right / held out over
    the seeds) from a cluster bootstrap over `clusters` (n_boot resamples, seed): [m, 2]."""
    uniq, inv = np.unique(clusters, return_inverse=True)
    sums, sizes = np.zeros((len(uniq), num.shape[1])), np.zeros((len(uniq), num.shape[1]))
    np.add.at(sums, inv, num)
    np.add.at(sizes, inv, den)
    rng = np.random.default_rng(seed)
    counts = np.stack([np.bincount(rng.integers(0, len(uniq), len(uniq)), minlength=len(uniq))
                       for _ in range(n_boot)]).astype(float)  # fmt: skip
    boot = (counts @ sums) / np.maximum(counts @ sizes, 1e-12)
    return np.percentile(boot, [2.5, 97.5], axis=0).T


def load_probes(name: str, s: str) -> dict | None:
    path = CACHE / name / f"{s}.npz"
    if not path.exists():
        return None
    z = np.load(path)
    keys = [str(k) for k in z["keys"]]
    return {"layers": [int(x) for x in z["layers"]], "right": dict(zip(keys, z["right"], strict=True)),
            "entity": z["entity"], "scene": z["scene"], "seconds": float(z["seconds"].sum())}  # fmt: skip


def summarize(pr: dict, n_boot: int) -> dict:
    """Per cell (position, target), feature and layer: the accuracy (rows x seeds), its cluster-bootstrap CI over the
    row's bridge entity; per cell and k the rule."""
    shares = {k: [round(float(v), 4) for v in pr["right"][k][:, 0].mean(1)] for k in pr["right"]
              if k.split("|")[1] == "share"}  # fmt: skip
    keys = sorted(k for k in pr["right"] if k not in shares)
    num = np.concatenate([pr["right"][k][:, 0].T for k in keys], axis=1)  # [n_rows, keys x layers]
    den = np.concatenate([pr["right"][k][:, 1].T for k in keys], axis=1)
    ci = cluster_ci(num, den, pr["entity"], n_boot)
    n_l = len(pr["layers"])
    acc: dict[str, dict] = collections.defaultdict(dict)
    for j, k in enumerate(keys):
        p, t, f = k.split("|")
        vals = pr["right"][k][:, 0].sum(1) / pr["right"][k][:, 1].sum(1)
        acc[f"{p}|{t}"][f] = {"acc": [round(float(v), 4) for v in vals],
                              "ci": [[round(float(a), 4), round(float(b), 4)] for a, b in ci[j * n_l : (j + 1) * n_l]]}  # fmt: skip
    rules = {}
    for cell, feats in acc.items():
        full = np.array(feats["full"]["acc"])
        rules[cell] = {}
        for k in KS:
            r = rule_label(full, np.array(feats[f"jpp{k}"]["acc"]), np.array(feats[f"rand{k}"]["acc"]))
            r["carry_layers"] = [pr["layers"][i] for i in r.pop("carry_layers_idx")]
            rules[cell][f"k{k}"] = r
    return {"layers": pr["layers"], "n_rows": len(pr["entity"]), "n_entities": len(set(pr["entity"])),
            "n_scenes": len(set(pr["scene"])), "acc": dict(acc), "rules": rules, "norm_share": shares,
            "cpu_seconds": pr["seconds"]}  # fmt: skip


def x52_check(name: str, target: str, states_root: Path, x52_root: Path) -> dict | None:
    """The main test's states against 52 B's cache (x52_answer_map read_main: [n, reader, O/S, B/E/Q/T, L, d]):
    per layer the lowest cosine over rows at B and T (same items in the same order, asserted)."""
    src = x52_root / X52_READ[target]
    if not (src / "states.npz").exists():
        return None
    order = json.loads((src / "gate.json").read_text())["order"]
    items = X.read_jsonl(states_root / name / "cases_main.jsonl")
    assert [it["scene"] for it in items] == order, "x52's items differ from the main test's"
    z = np.load(src / "states.npz")
    old, old_layers = z["h"], [int(x) for x in z["layers"]]
    h = np.load(states_root / name / "states_main_h.npy", mmap_mode="r")
    m = json.loads((states_root / name / "manifest.json").read_text())
    out = {}
    for li, la in enumerate(m["layers"]):
        if la not in old_layers:
            continue
        lo = old_layers.index(la)
        pairs = {"B": (h[li][:, :, 0], old[:, 0, :, 0, lo]), "T_lookup": (h[li][:, :, 1], old[:, 0, :, 3, lo]),
                 "T_recall": (h[li][:, :, 2], old[:, 1, :, 3, lo])}  # fmt: skip
        out[la] = {}
        for p, (a, b) in pairs.items():
            a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
            cos = (a * b).sum(-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1) + 1e-30)
            out[la][p] = round(float(cos.min()), 5)
    return out


def figure(results: dict, s: str, path: Path) -> None:
    """Accuracy by layer, one panel per target (columns) per model x position (rows); four feature lines (J++, random,
    PCA: k = 25 solid, k = 100 dashed; full; chance dotted)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts import story_style as SS

    col = {"full": "#111111", "jpp": SS.COL["lookup"], "rand": "#9a9a9a", "pca": SS.COL["value"], "chance": "#cccccc"}
    models = [t for t in MODELS if results.get(t, {}).get(s)]
    rows = [(t, p) for t in models for p in PROBE_POS]
    fig, axes = plt.subplots(len(rows), len(TARGETS), figsize=(13, 2.3 * len(rows) + 1.2), sharey=True, squeeze=False)
    for i, (t, p) in enumerate(rows):
        res = results[t][s]
        layers = res["layers"]
        for j, tg in enumerate(TARGETS):
            ax = axes[i][j]
            feats = res["acc"][f"{p}|{tg}"]
            ax.plot(layers, feats["chance"]["acc"], ":", color=col["chance"], lw=1.2)
            ax.plot(layers, feats["full"]["acc"], "-", color=col["full"], lw=1.8)
            for k, ls in zip(KS, ("-", "--"), strict=True):
                for fam in ("rand", "pca", "jpp"):
                    ax.plot(layers, feats[f"{fam}{k}"]["acc"], ls, color=col[fam], lw=1.5 if fam == "jpp" else 1.1)
            short = {"J-space blind to X": "blind", "J-space carries X": "carries", "in between": "between"}
            lab = " / ".join(short[res["rules"][f"{p}|{tg}"][f"k{k}"]["label"]] for k in KS)
            ax.set_title(f"{TARGET_SHORT[tg]}  [{lab}]", fontsize=8.5)
            ax.axhline(0.8, color="#e0e0e0", lw=0.8, zorder=0)
            ax.set_ylim(-0.02, 1.02)
            ax.tick_params(labelsize=8)
            if j == 0:
                ax.set_ylabel(f"{NAMES[t]}\n{'bridge word' if p == 'B' else 'last token'}", fontsize=9)
            if i == len(rows) - 1:
                ax.set_xlabel("layer", fontsize=9)
    handles = [plt.Line2D([], [], color=col["full"], lw=1.6, label="full residual"),
               plt.Line2D([], [], color=col["jpp"], lw=1.4, label="J++ lens part"),
               plt.Line2D([], [], color=col["rand"], lw=1.1, label="random subspace"),
               plt.Line2D([], [], color=col["pca"], lw=1.1, label="PCA top-k"),
               plt.Line2D([], [], color="#555555", ls="-", label="k = 25"),
               plt.Line2D([], [], color="#555555", ls="--", label="k = 100"),
               plt.Line2D([], [], color=col["chance"], ls=":", label="chance (majority)")]  # fmt: skip
    fig.legend(handles=handles, loc="upper center", ncol=7, fontsize=8.5, frameon=False, bbox_to_anchor=(0.5, 1.0))
    fig.suptitle(f"53.2, the monitor test: probe accuracy by layer, {SET_TEXT[s]} (held-out entities for (b), (c); "
                 "held-out scenes for (a), (d); rule label per panel: k = 25 / 100; UNVERIFIED)", fontsize=10,
                 y=1.0 - 0.35 / (2.3 * len(rows) + 1.2))  # fmt: skip
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.75 / (2.3 * len(rows) + 1.2)))
    fig.savefig(path, dpi=110)
    plt.close(fig)


def stage_verdict(states_root: Path, x52_root: Path, n_boot: int = X.N_BOOT) -> Path:
    """CPU: per model and dataset the accuracies, CIs and the rule; one figure per dataset; verdict.md and the json."""
    from bridge_jspace.utils import git_state

    results: dict[str, dict] = {}
    checks: dict[str, Any] = {}
    for target in MODELS:
        name = RUNS[target]
        for s in SETS:
            pr = load_probes(name, s)
            if pr is None:
                continue
            results.setdefault(target, {})[s] = summarize(pr, n_boot)
        if target in results and (states_root / name / "states_main_h.npy").exists():
            checks[target] = x52_check(name, target, states_root, x52_root)
    assert results, "no probes in cache/x53_monitor/: run the probe stage first"
    out = RESULTS / f"x53_monitor-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True, exist_ok=False)
    figs = []
    for s in SETS:
        if any(s in r for r in results.values()):
            path = out / f"x53_monitor_{s}.png"
            figure(results, s, path)
            figs.append(path.name)
    blob = {"exp": EXP, "test": "53.2 (the monitor test)", "spec": "jobs/c3/batch53.yaml (53.2); jobs/c3/x53_monitor_*.yaml",
            "prediction": NO_PREDICTION, "status": "UNVERIFIED", "rule": RULE, "targets": TARGET_TEXT,
            "groupings": {t: GROUP_TEXT[GROUP_BY[t]] for t in TARGETS}, "positions": PROBE_POS_TEXT,
            "features": FEATURE_TEXT, "probe": {"C": C_REG, "seeds": N_SEEDS, "folds": N_FOLDS,
                                                "cv": "per seed a random assignment of the groups to the folds",
                                                "objective": "0.5 ||W||^2 + C x summed log-loss, intercept unpenalised",
                                                "standardised": "training rows' mean and sd"},
            "bootstrap": {"n": n_boot, "seed": X.BOOT_SEED, "cluster": "the row's bridge entity"},
            "runs": {t: RUNS[t] for t in results}, "x52_check_min_cosine": checks, "figures": figs,
            "code": git_state(), "results": results,
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
    (out / "x53_monitor.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "verdict.md").write_text("\n".join(verdict_lines(blob)) + "\n")
    print(f"wrote {out}", flush=True)
    return out


def verdict_lines(blob: dict) -> list[str]:
    res = blob["results"]
    lines = ["# 53.2, the monitor test: what a J-space readout can decode vs the full state", "",
             f"UNVERIFIED. {NO_PREDICTION}. Spec: {blob['spec']}.", "", f"Rule (verbatim): {RULE}", "",
             "As computed: per model, dataset, position, target and k, on point estimates (accuracy over rows and "
             f"{N_SEEDS} seeds of {N_FOLDS}-fold CV, each seed a random assignment of the groups to the folds), over "
             "every cached layer (every second layer from L0); logistic "
             f"probes, C = {C_REG} for every feature (sklearn's objective, standardised features, scipy L-BFGS); "
             "(b), (c) on held-out entities; (a), (d) on held-out scenes (a held-out entity is an unseen class there). "
             f"CIs: cluster bootstrap over the bridge entity ({blob['bootstrap']['n']:,}, seed 0).", ""]  # fmt: skip
    lines += ["## Labels", "",
              "Notes column (beside the rule, not part of it): 'random reads it too' = blind by the rule while J++ "
              "itself reaches >= 0.8 (the random subspace decodes X as well, so the label says J++ adds nothing over "
              "a random subspace, not that J++ cannot read X); 'full < 0.8' = the full residual never reaches 0.8, so "
              "neither 'blind' nor 'carries' can open.", "",
              "| model | dataset | position | target | k = 25 | k = 100 | full max | J++25 max (gap to random max) | "
              "J++100 max (gap max) | PCA25 / PCA100 max | notes |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in MODELS:
        for s in SETS:
            r = res.get(t, {}).get(s)
            if not r:
                continue
            for p in PROBE_POS:
                for tg in TARGETS:
                    ru = r["rules"][f"{p}|{tg}"]
                    feats = r["acc"][f"{p}|{tg}"]
                    pca = " / ".join(f"{max(feats[f'pca{k}']['acc']):.2f}" for k in KS)
                    notes = [
                        f"k = {k}: random reads it too"
                        for k in KS
                        if ru[f"k{k}"]["label"] == LABELS[0] and ru[f"k{k}"]["jpp_max"] >= CARRY_MIN - EPS
                    ]
                    if not ru["k25"]["full_reaches_0.8"]:
                        notes.append("full < 0.8")
                    lines.append(f"| {NAMES[t]} | {s} (n {r['n_rows']} rows, {r['n_entities']} entities) | {p} | "
                                 f"{TARGET_TEXT[tg]} | {ru['k25']['label']} | {ru['k100']['label']} | "
                                 f"{ru['k25']['full_max']:.2f} | {ru['k25']['jpp_max']:.2f} ({ru['k25']['gap_max']:+.2f}) "
                                 f"| {ru['k100']['jpp_max']:.2f} ({ru['k100']['gap_max']:+.2f}) | {pca} | "
                                 f"{'; '.join(notes)} |")  # fmt: skip
    missing = [f"{NAMES[t]} {s}" for t in MODELS for s in SETS if not res.get(t, {}).get(s)]
    lines += ["", f"Not yet probed (states not pulled): {', '.join(missing) or 'none'}.", ""]
    lines += ["## The main test's states vs 52 B's cache (lowest cosine over rows, any layer)", ""]
    for t, c in blob["x52_check_min_cosine"].items():
        if c:
            lo = min(v for la in c.values() for v in la.values())
            lines.append(f"- {NAMES[t]}: {lo:.5f} over {len(c)} layers (B, T lookup, T recall)")
        else:
            lines.append(f"- {NAMES[t]}: 52 B's states not found locally")
    lines += ["", "## Where each label is decided", "",
              "carries: the first layer with J++ >= 0.8 and J++ - random >= 0.3; otherwise the layer of the largest "
              "J++ - random gap. Accuracy [95% CI].", "",
              "| model | dataset | position | target | k | label | layer | full | J++ | random | PCA | chance |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in MODELS:
        for s in SETS:
            r = res.get(t, {}).get(s)
            if not r:
                continue
            for p in PROBE_POS:
                for tg in TARGETS:
                    feats = r["acc"][f"{p}|{tg}"]
                    for k in KS:
                        ru = r["rules"][f"{p}|{tg}"][f"k{k}"]
                        if ru["carry_layers"]:
                            li = r["layers"].index(ru["carry_layers"][0])
                        else:
                            li = int(np.argmax(np.array(feats[f"jpp{k}"]["acc"]) - np.array(feats[f"rand{k}"]["acc"])))
                        cell = [fmt_acc(feats[f], li) for f in ("full", f"jpp{k}", f"rand{k}", f"pca{k}", "chance")]
                        lines.append(f"| {NAMES[t]} | {s} | {p} | {TARGET_SHORT[tg]} | {k} | {ru['label']} | "
                                     f"L{r['layers'][li]} | " + " | ".join(cell) + " |")  # fmt: skip
    lines += ["", "## Beside: each part's share of the state's squared norm (median over layers)", "",
              "The J++ part is fit to each state (OMP picks the atoms that match it), the random subspace is fixed: "
              "the shares say how much of the state each feature keeps.", "",
              "| model | dataset | row set | J++25 | J++100 | random25 | random100 |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for t in MODELS:
        for s in SETS:
            r = res.get(t, {}).get(s)
            if not r or not r.get("norm_share"):
                continue
            for pos in POS:
                vals = [r["norm_share"].get(f"{pos}|share|{f}") for f in ("jpp25", "jpp100", "rand25", "rand100")]
                if all(v is not None for v in vals):
                    lines.append(
                        f"| {NAMES[t]} | {s} | {pos} | " + " | ".join(f"{np.median(v):.3f}" for v in vals) + " |"
                    )
    n_text = "; ".join(f"{NAMES[t]} {s} {r['n_rows']} rows ({r['n_scenes']} scenes, {r['n_entities']} bridge entities)"
                       for t in MODELS for s, r in res.get(t, {}).items())  # fmt: skip
    lines += ["", "## Report", "",
              f"EXP x53_monitor (53.2) @ {blob['code'].get('sha', '?')[:8]} | models {', '.join(NAMES[t] for t in res)} | "
              f"n: {n_text} | seeds: probe splits 0-4, random subspaces 888 + layer + 1000 x seed, bootstrap 0", "",
              "Claim tested: a probe on the J++ lens part of the state decodes (a)-(d) as well as the full residual "
              "(carries), or no better than a random subspace of the same size while the full residual decodes it "
              "(blind).", "",
              "Three dumbest ways this could be wrong:",
              "1) The J++ part is fit to each state while the random subspace is fixed, so J++ keeps more of the state "
              "(see the norm shares) and can beat random on energy alone, not because the lens is special. Checked "
              "beside: PCA top-k (a fixed subspace that keeps the most variance) is drawn in every panel; a 'carries' "
              "where PCA matches J++ is not lens-specific.",
              "2) (a) and (d) are probed on held-out scenes, not entities (a held-out entity is an unseen class); the "
              "probe can then read the bridge's identity and map it to the recall's answer, so (d) at the bridge word "
              "is identity, not the answer computed. Not checked beyond the grouping; (b) and (c) are on held-out "
              "entities.",
              "3) One C for every feature: the full residual and J++ (fit in the training span, up to n_train "
              "dimensions) and the k-dimensional random / PCA features are regularised differently in effect; a "
              "low full-residual ceiling (e.g. the slot at the bridge word) can be the probe, not the state. Not "
              "checked (the brief fixes the same regularisation).", "",
              "For the human to verify: the rule from the per-layer accuracies in x53_monitor.json "
              "(results[<model>][<set>]['acc']['<B|T>|<a-d>'][<feature>]); one cell end to end by rerunning "
              "`scripts/x53_monitor.py probe --name <run> --states-root <dir with the pulled states>` (deterministic; "
              "cache/x53_monitor/<run>/<set>.npz holds per row [right, held out] over the 5 seeds).", "",
              "Status: UNVERIFIED (exploration day; nothing into the README).", "",
              f"Figures: {', '.join(blob['figures'])} (accuracy by layer; columns the four targets, rows model x "
              "position; full black, J++ purple, random grey, PCA green; k = 25 solid, k = 100 dashed; chance "
              "dotted). Per-layer accuracies, CIs and chance: x53_monitor.json.", ""]  # fmt: skip
    return lines


def fmt_acc(feat: dict, li: int) -> str:
    lo, hi = feat["ci"][li]
    return f"{feat['acc'][li]:.2f} [{lo:.2f}, {hi:.2f}]"


# ---- CLI ------------------------------------------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan", help="CPU (tokenizer): items, labels, counts for BJ_TARGET")
    p = sub.add_parser("run", help="GPU: states and J++ parts")
    p.add_argument("--name", required=True)
    p = sub.add_parser("probe", help="CPU: one run's probes into cache/x53_monitor/<run>/")
    p.add_argument("--name", required=True)
    p.add_argument("--states-root", type=Path, default=RESULTS, help="where the run's states are (default results/)")
    p.add_argument("--sets", default=",".join(SETS))
    p.add_argument("--workers", type=int, default=WORKERS)
    p.add_argument("--pass", dest="pass_", default="base", choices=tuple(PASSES))
    p = sub.add_parser("atom-ids", help="CPU: the atoms the fixed J++ subspaces need (for the box's atoms stage)")
    p.add_argument("--name", required=True)
    p.add_argument("--states-root", type=Path, default=RESULTS)
    p = sub.add_parser("atoms", help="GPU: the fixed J++ subspaces' atom vectors into results/x53_monitor/<run>_atoms/")
    p.add_argument("--name", required=True, help="the atoms run: <source>_atoms")
    p.add_argument("--source", required=True, help="the forward run whose fixed_atom_ids.json it reads")
    p = sub.add_parser("verdict", help="CPU: the rule, the figures, results/x53_monitor/x53_monitor-<UTC>/")
    p.add_argument("--states-root", type=Path, default=RESULTS)
    p.add_argument("--x52-root", type=Path, default=pins.RESULTS_DIR / "x52_answer_map")
    p.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.cmd == "plan":
        stage_plan()
    elif a.cmd == "run":
        stage_run(a.name)
    elif a.cmd == "probe":
        stage_probe(a.name, a.states_root, tuple(a.sets.split(",")), a.workers, a.pass_)
    elif a.cmd == "atom-ids":
        stage_atom_ids(a.name, a.states_root)
    elif a.cmd == "atoms":
        stage_atoms(a.name, a.source)
    elif a.cmd == "verdict":
        stage_verdict(a.states_root, a.x52_root, a.n_boot)


if __name__ == "__main__":
    main()
