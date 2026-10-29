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
SET_TEXT = {"main": "our main test (X0's scenes)", "json": "the varied scenes, JSON format (x0b_v2)"}
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


BUILD = {"main": lambda tok, target: main_items(tok, target), "json": lambda tok, target: json_items(tok)}


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


def stage_run(name: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "x53 reads the sources' chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in MODELS, f"x53_monitor runs on {MODELS}, not {target}"
    n_layers = pins.TARGETS[target]["n_layers"]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    inputs = [SPEC, pins.DATA_DIR / "tasks_v2" / JSON_SET / "items.jsonl"]
    m = manifest(name, target, {"inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p) for p in inputs},
                                "layers_candidate": list(layers_for(n_layers)), "n_layers": n_layers})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    lens = JLens(model, "jpp")
    layers = tuple(la for la in layers_for(n_layers) if la in lens.source_layers)
    assert layers, "the J++ lens has no map at any candidate layer"
    sets: dict[str, Any] = {}
    for s in SETS:
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


# ---- CLI ------------------------------------------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan", help="CPU (tokenizer): items, labels, counts for BJ_TARGET")
    p = sub.add_parser("run", help="GPU: states and J++ parts")
    p.add_argument("--name", required=True)
    a = ap.parse_args()
    if a.cmd == "plan":
        stage_plan()
    elif a.cmd == "run":
        stage_run(a.name)


if __name__ == "__main__":
    main()
