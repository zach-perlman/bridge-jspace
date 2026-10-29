"""x53_attnblock (test 53.4; Dan 29 Oct ~10:05, jobs/c3/batch52.yaml `lightning_attn_block`, kept unchanged as 53.4 in
jobs/c3/batch53.yaml; the rule fixed then, no prediction): does Lightning's lookup read the bridge word through
attention blocks 19 and 26?

Items: Lightning's conflict run (x0_necessity nem35l_x52_conflict: X0's main test, two people swap picks, chat; the 60
dev scenes already kept out by that run), its items at L = the committed layer (14, BJ_PREDICTED_LAYER), in its order,
rebuilt and checked id by id. The whole change Δ = h_alt - h_org at the bridge word (one token; X0's position) at block
L's output, one forward per prompt (X0's). Reads: X0's chat read on the org prompt (a digit's space token appended; the
top token over the vocabulary), lookup and recall, with Δ added at the bridge word at L ("whole") or nothing ("clean").
Switch = the top token is the alt answer's first token (X0's).

Blocking (bridge_jspace.knockout.knock_out, 47.6's mechanics through x47_edges.forward: uncached forwards, mode value):
in the listed attention blocks, every position after the source cannot attend to it: those query -> key logits are -inf
in every head, so each such query's softmax renormalises over the keys it still reads; every other pair and every other
block as is (Lightning's Mamba-2 and MoE blocks untouched). Arms (rows of one batched forward per item and reader, each
arm clean and whole; equal-length rows):
  none     no block (the whole change's switches: S_whole)
  b19      (i)   block 19 only, source = the bridge word
  b26      (ii)  block 26 only, source = the bridge word
  both     (iii) blocks 19 and 26, source = the bridge word
  after    (iv)  every softmax-attention block after L (Lightning at L14: 19 / 26 / 33 / 42; from the config, asserted
                 to hold 19 and 26), source = the bridge word
  control  (v)   blocks 19 and 26, source = a random non-bridge token of the bridge's sentence (X0's bind_bridge
                 statement: the asked pick sentence; tokens overlapping the sentence, the bridge word's excluded), one per
                 scene (random.Random keyed by CONTROL_SEED and the scene); destinations every position after it
Edges per row (destinations x blocks) are stored; the control's differ from (iii)'s by the gap between the two sources.

Rule (verbatim, RULE) and how it is computed (AS_COMPUTED). The recall's numbers are reported beside (no label). The
clean rows give each arm's collateral damage (the clean answer lost). Cluster-bootstrap CIs over the bridge entities
(10,000, seed 0; paired across arms) beside the points. Every result UNVERIFIED.

BJ_TARGET=nemotron-3.5-lightning BJ_PREDICTED_LAYER=14 uv run python scripts/x53_attnblock.py plan          # CPU
BJ_TARGET=nemotron-3.5-lightning BJ_PREDICTED_LAYER=14 uv run python scripts/x53_attnblock.py run --name nem35l_x53_attnblock
uv run python scripts/x53_attnblock.py verdict --name nem35l_x53_attnblock                                   # CPU
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.knockout import FULL
from scripts import x0_necessity as X

EXP = "x53_attnblock"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch52.yaml"  # the rule's text (lightning_attn_block)
BATCH = pins.REPO_ROOT / "jobs" / "c3" / "batch53.yaml"  # 53.4: "the spec sent at 09:20, unchanged"
TARGET = "nemotron-3.5-lightning"
RUN = "nem35l_x53_attnblock"
BLOCKS = (19, 26)  # Dan's two blocks
ARMS = ("none", "b19", "b26", "both", "after", "control")
PATCHES = ("clean", "whole")
RULE_ARM = {"i": "b19", "ii": "b26", "iii": "both", "iv": "after", "v": "control"}
ARM_TEXT = {"none": "no block", "b19": "(i) block 19 only", "b26": "(ii) block 26 only", "both": "(iii) blocks 19 and 26",
            "after": "(iv) every attention block after L", "control": "(v) blocks 19 and 26, a random non-bridge token "
            "of the bridge's sentence as the source"}  # fmt: skip
CONTROL_SEED = 5346
TWO, CONTROL_MAX, ONE, NOT_ATTN = 0.6, 0.15, 0.6, 0.3
EPS = 1e-9  # a value exactly at a bar counts as at the bar
NO_PREDICTION = "no prediction (Dan, 29 Oct ~10:05: the rule fixed then, before any run)"
LABELS = ("read through two blocks", "one block", "not through attention at the bridge", "in between")
RULE = (
    "\"read through two blocks\" if (iii) cuts the lookup's switches by >= 0.6 of the whole change's and (v) by <= "
    '0.15; "one block" if (i) or (ii) alone cuts >= 0.6; "not through attention at the bridge" if (iv) cuts < 0.3 (the '
    "Mamba state carries it); else in between."
)
AS_COMPUTED = (
    "cut(x) = 1 - S_x / S_whole on the lookup, S_x = the share of items whose lookup switches under the whole change "
    "with arm x's block, S_whole = the same with no block (arm none), all in this run's forwards; point estimates "
    f"decide, EPS {EPS} at the bars ('< 0.3' strict). The clauses are checked in the rule's order and the first that "
    "holds is the label; any other clause that also holds is listed beside it (flagged for Dan: the rule does not say "
    "which wins). S_whole = 0: not tested. X0's validity (S_whole >= 0.30 and >= 30 items switched) is reported, not a "
    "gate (the rule has none)."
)


# ---- pure (CPU) ---------------------------------------------------------------------------------------------------


def arm_layers(kinds: list[str], layer: int) -> dict[str, list[int]]:
    """Each blocking arm's blocks: Dan's two, both, and every softmax-attention block after `layer` (both of his
    asserted among them)."""
    after = [la for la, k in enumerate(kinds) if k == FULL and la > layer]
    assert set(BLOCKS) <= set(after), f"blocks {BLOCKS} are not all softmax attention after L{layer}: {after}"
    a, b = BLOCKS
    return {"b19": [a], "b26": [b], "both": [a, b], "after": after, "control": [a, b]}


def control_position(scene: str, candidates: list[int], seed: int = CONTROL_SEED) -> int:
    """The control's source: one of the sentence's non-bridge positions, drawn per scene."""
    assert candidates, f"{scene}: no non-bridge token in the bridge's sentence"
    return random.Random(f"x53_attnblock|{seed}|{scene}").choice(sorted(candidates))


def knock_of(arm: str, sets: dict[str, list[int]], pos: int, control: int, length: int) -> tuple | None:
    """x47_edges.forward's knock entry (blocks, sources, destinations) of one arm on a prompt of `length` tokens:
    every position after the source is a destination."""
    if arm == "none":
        return None
    src = control if arm == "control" else pos
    assert 0 < src < length - 1, f"source {src} in a prompt of {length}"
    return sets[arm], [src], list(range(src + 1, length))


def cut(s_arm: float, s_whole: float) -> float:
    return 1.0 - s_arm / s_whole if s_whole > 0 else math.nan


def label(cuts: dict[str, float]) -> dict[str, Any]:
    """The rule on the lookup's cuts per rule arm (i .. v): every clause, the label (first clause holding, in the
    rule's order) and the other clauses that hold."""
    if any(math.isnan(cuts[k]) for k in RULE_ARM):
        return {"label": "not tested (nothing switched under the whole change)", "clauses": {}, "also": []}
    clauses = {
        LABELS[0]: cuts["iii"] >= TWO - EPS and cuts["v"] <= CONTROL_MAX + EPS,
        LABELS[1]: cuts["i"] >= ONE - EPS or cuts["ii"] >= ONE - EPS,
        LABELS[2]: cuts["iv"] < NOT_ATTN - EPS,
    }
    held = [k for k, v in clauses.items() if v]
    return {"label": held[0] if held else LABELS[3], "clauses": clauses, "also": held[1:]}


# ---- items (tokenizer and the stored run) ---------------------------------------------------------------------------


def sentence_tokens(tok, item: dict) -> tuple[list[int], list[int], list[int]]:
    """The org chat prompt's ids, the token positions of the bridge's sentence (X0's bind_bridge statement) and of the
    bridge word in it, found as x0_necessity.encode_bridge finds the word."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP

    context = item["context"]
    text = X.render(tok, item, "chat", context)
    enc = raw_encoding(tok, text, offsets=True)
    sentence = SP.tasks_statements(item)["bind_bridge"]
    s0 = text.index(context) + SP.find_sentence(context, sentence)
    w0 = s0 + sentence.rindex(item["bridge"])
    offs = enc["offset_mapping"]
    return (
        list(enc["input_ids"]),
        SP.tokens_in(offs, s0, s0 + len(sentence)),
        SP.tokens_in(offs, w0, w0 + len(item["bridge"])),
    )


def build_items(tok, target: str = TARGET) -> tuple[list[dict], dict]:
    """The conflict run's items at L in its order (rebuilt; ids and position asserted equal to its cases), each with
    its bridge sentence's positions, the control's source and the stored whole-change switch per reader."""
    from scripts import tasks_v2 as T
    from scripts import x45b_binding as B
    from scripts import x47_cumulative as C

    src = X.RESULTS / B.MAIN_RUN[target]
    layer = X.PREDICTED[target]
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{src.name} is not {target}'s"
    assert m["predicted"] == layer, f"{src.name}: layer {m['predicted']}, not {layer} (BJ_PREDICTED_LAYER)"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {src.name}"
    scenes, stored = C.stored_whole(src, layer)
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
    with B.x0_alt(m.get("alt") or "cf", ("chat",)):
        cases, _ = X.build_cases(tok, m["set"])
    rebuilt = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, multi = [], 0
    for s in scenes:
        c = rebuilt[s]
        assert c["pos"] == old[s]["pos"], f"{s}: the bridge position moved since {src.name}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[s]["readers"][w]["ids"], f"{s}: {w}'s ids changed since {src.name}"
        ids, sent, word = sentence_tokens(tok, by_id[c["readers"][X.LOOKUP]["id"]])
        assert ids == c["readers"][X.LOOKUP]["ids"]["org"], f"{s}: the rebuilt prompt differs from the run's"
        assert word == [c["pos"]], f"{s}: the bridge word is not at the run's position"
        end = max(sent) + 1
        for w in X.READERS:
            assert c["readers"][w]["ids"]["org"][:end] == ids[:end], f"{s}: {w}'s prompt differs in the bridge sentence"
        cands = [p for p in sent if p not in word and p > 0]
        multi += len(word) > 1
        out.append({**c, "sentence": sent, "control": control_position(s, cands), "candidates": len(cands),
                    "stored_whole": stored[s]})  # fmt: skip
    counts = {"source": src.name, "set": m["set"], "layer": layer, "items": len(out),
              "entities": len({it["bridge"] for it in out}), "control_before_bridge": sum(it["control"] < it["pos"] for it in out),
              "sentence_tokens": [min(len(it["sentence"]) for it in out), max(len(it["sentence"]) for it in out)] if out else None}  # fmt: skip
    return out, counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def manifest(name: str, why: str, sets: dict[str, list[int]], counts: dict) -> dict:
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state

    src = X.RESULTS / counts["source"]
    return {"exp": EXP, "run": name, "why": why, "test": "53.4", "spec": "jobs/c3/batch52.yaml (lightning_attn_block); "
            "jobs/c3/batch53.yaml (53.4); jobs/c3/x53_4_lightning_attnblock.yaml",
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "model": pins.model_pin(), "switches": switches(), "code": git_state(),
            "inputs": {str(p.relative_to(pins.REPO_ROOT)): pins.sha256_file(p)
                       for p in (SPEC, BATCH, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")
                       if p.exists()},
            "items": counts, "layer": counts["layer"], "arms": list(ARMS), "arm_text": ARM_TEXT, "arm_layers": sets,
            "patches": {"clean": "nothing added", "whole": "Δ added at the bridge word at L (AddRows' arithmetic)"},
            "blocking": "knockout.knock_out (mode value) via x47_edges.forward: in the arm's blocks, every position after "
                        "the source has its logits to the source at -inf in every head; uncached forwards",
            "read": "X0's chat read (the org prompt with a digit's space token appended; top token over the vocabulary; "
                    "switch = the alt answer's first token)",
            "seeds": {"control": f"random.Random('x53_attnblock|{CONTROL_SEED}|<scene>')", "bootstrap": X.BOOT_SEED},
            "order": {"items": "the conflict run's item order",
                      "rows": "per item and reader one forward of len(ARMS) x 2 rows: arm-major, clean then whole"},
            "rule": RULE, "as_computed": AS_COMPUTED, "prediction": NO_PREDICTION}  # fmt: skip


def stage_plan() -> dict:
    """CPU: the items, the control sources and the arms' blocks from the target's config, counts printed."""
    from bridge_jspace.knockout import config_layer_kinds
    from scripts import x45m

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    tok = x45m.tokenizer()
    its, counts = build_items(tok)
    sets = arm_layers(config_layer_kinds(_config()), X.PREDICTED[TARGET])
    out = {"counts": counts, "arm_layers": sets}
    print(json.dumps(out, indent=1))
    for it in its[:3]:
        ids = it["readers"][X.LOOKUP]["ids"]["org"]
        print(it["scene"], "bridge", repr(tok.decode([ids[it["pos"]]])), "control", repr(tok.decode([ids[it["control"]]])),
              "sentence", repr(tok.decode([ids[p] for p in it["sentence"]])))  # fmt: skip
    return out


def _config():
    from huggingface_hub import try_to_load_from_cache
    from transformers import AutoConfig

    t = pins.TARGETS[TARGET]
    path = try_to_load_from_cache(t["repo"], "config.json", revision=t["revision"])
    assert isinstance(path, str), f"{t['repo']}: config not cached"
    return AutoConfig.from_pretrained(str(Path(path).parent))


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace.knockout import layer_kinds
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import x47_edges as E

    assert pins.TARGET == TARGET, f"BJ_TARGET={pins.TARGET}, not {TARGET}"
    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    model = load_model()
    tok = model.tokenizer
    layer = X.PREDICTED[TARGET]
    sets = arm_layers(layer_kinds(model), layer)
    its, counts = build_items(tok)
    (out / "manifest.json").write_text(json.dumps(manifest(name, why, sets, counts), indent=1) + "\n")
    print(json.dumps({"items": counts, "arm_layers": sets}), flush=True)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    specs = [(a, p) for a in ARMS for p in PATCHES]
    with (out / "items.jsonl").open("w") as f:
        for it in its:
            ids = it["readers"][X.LOOKUP]["ids"]["org"]
            f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "pos": it["pos"], "control": it["control"],
                                "sentence": it["sentence"], "candidates": it["candidates"],
                                "bridge_token": tok.decode([ids[it["pos"]]]), "control_token": tok.decode([ids[it["control"]]]),
                                "sentence_text": tok.decode([ids[p] for p in it["sentence"]]),
                                "stored_whole": it["stored_whole"]}) + "\n")  # fmt: skip
    t0 = time.time()
    with torch.no_grad(), (out / "outcomes.jsonl").open("w") as f:
        for it in progress(its, "attention blocks (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][it["pos"]]
                 for v in ("org", "alt")}  # fmt: skip
            delta = h["alt"] - h["org"]
            for w, rd in it["readers"].items():
                prompt = rd["ids"]["org"] + it["space"]
                n = len(prompt)
                adds = [[(layer, it["pos"], delta)] if p == "whole" else None for _, p in specs]
                knock = [knock_of(a, sets, it["pos"], it["control"], n) for a, _ in specs]
                logits, _ = E.forward(model, [prompt] * len(specs), adds, knock)
                assert logits is not None
                for (a, p), k, lg in zip(specs, knock, logits, strict=True):
                    row = X.read_row(lg, rd, digits)
                    f.write(json.dumps({"scene": it["scene"], "entity": it["bridge"], "reader": w, "arm": a, "patch": p,
                                        **row, "top_text": tok.decode([row["top"]]),
                                        "edges": len(k[0]) * len(k[2]) if k else 0}) + "\n")  # fmt: skip
    print(f"{len(its)} items in {time.time() - t0:.0f} s -> {out}", flush=True)
    return out


# ---- verdict (CPU) --------------------------------------------------------------------------------------------------


def reader_numbers(rows: list[dict], reader: str, n_boot: int = X.N_BOOT) -> dict:
    """One reader: per arm the switched share under the whole change and the clean answer kept (top = org answer's
    first token) without it; the cut of each blocking arm vs none with a paired cluster-bootstrap CI."""
    by = {(r["scene"], r["arm"], r["patch"]): r for r in rows if r["reader"] == reader}
    scenes = list(dict.fromkeys(r["scene"] for r in rows if r["reader"] == reader))
    ents = [by[(s, "none", "whole")]["entity"] for s in scenes]
    sw = {a: [int(by[(s, a, "whole")]["switched"]) for s in scenes] for a in ARMS}
    kept = {a: [int(by[(s, a, "clean")]["role"] == "A") for s in scenes] for a in ARMS}
    r = X.resampled_rates(sw, ents, n_boot)
    s = {a: float(np.mean(v)) for a, v in sw.items()}
    cuts, cis = {}, {}
    for a in ARMS[1:]:
        cuts[a] = cut(s[a], s["none"])
        cis[a] = (
            [round(x, 3) for x in X.interval(1.0 - r[a] / np.where(r["none"] > 0, r["none"], np.nan))]
            if s["none"] > 0
            else None
        )
    edges = {a: [by[(sc, a, "whole")]["edges"] for sc in scenes] for a in ARMS[1:]}
    return {"n": len(scenes), "entities": len(set(ents)), "switched": {a: int(sum(v)) for a, v in sw.items()},
            "S": {a: round(v, 4) for a, v in s.items()}, "cut": {a: round(v, 4) for a, v in cuts.items()},
            "cut_ci": cis, "clean_kept": {a: round(float(np.mean(v)), 4) for a, v in kept.items()},
            "x0_valid": bool(s["none"] >= X.VALID_S and sum(sw["none"]) >= X.VALID_N),
            "edges_median": {a: float(np.median(v)) for a, v in edges.items()}}  # fmt: skip


def agreement(rows: list[dict], items: list[dict]) -> dict:
    """This run's whole-change switch (no block) vs the conflict run's stored one, per reader (Lightning's numerics
    depend on batch composition: descriptive)."""
    stored = {it["scene"]: it["stored_whole"] for it in items}
    out = {}
    for w in X.READERS:
        pairs = [(int(r["switched"]), stored[r["scene"]][w]) for r in rows
                 if r["reader"] == w and r["arm"] == "none" and r["patch"] == "whole"]  # fmt: skip
        out[w] = {"agree": round(float(np.mean([a == b for a, b in pairs])), 4), "this_run": sum(a for a, _ in pairs),
                  "stored": sum(b for _, b in pairs), "n": len(pairs)}  # fmt: skip
    return out


def fmt(x: float, ci: list | None = None) -> str:
    return (
        "nan"
        if x is None or (isinstance(x, float) and math.isnan(x))
        else f"{x:.3f}" + (f" [{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "")
    )


def example_lines(rows: list[dict], items: list[dict], k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items (fixed seed): bridge and control tokens, the lookup's top token under the whole change per arm."""
    idx = sorted(random.Random(seed).sample(range(len(items)), min(k, len(items))))
    by = {(r["scene"], r["arm"]): r for r in rows if r["reader"] == X.LOOKUP and r["patch"] == "whole"}
    out = [f"Examples ({len(idx)} random items, seed {seed}; the lookup's top token under the whole change, '*' = "
           "switched):"]  # fmt: skip
    for i in idx:
        it = items[i]
        tops = ", ".join(f"{a} {by[(it['scene'], a)]['top_text']!r}{'*' if by[(it['scene'], a)]['switched'] else ''}"
                         for a in ARMS)  # fmt: skip
        out.append(f"- {it['scene']}: sentence {it['sentence_text']!r}, bridge {it['bridge_token']!r}, control "
                   f"{it['control_token']!r}; {tops}")  # fmt: skip
    return out


def stage_verdict(name: str = RUN, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "items.jsonl")
    nums = {w: reader_numbers(rows, w, n_boot) for w in X.READERS}
    lk = nums[X.LOOKUP]
    res = label({k: lk["cut"][a] for k, a in RULE_ARM.items()})
    out = RESULTS / f"{EXP}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    agree = agreement(rows, items)
    lines = [f"x53_attnblock (Lightning, L{m['layer']}; run {name}); {NO_PREDICTION}; UNVERIFIED", "",
             f"Rule (verbatim): {RULE}", f"As computed: {AS_COMPUTED}", "",
             f"Label (lookup): {res['label']}" + (f"; also holds: {', '.join(res['also'])}" if res["also"] else ""),
             f"Clauses: {json.dumps(res['clauses'])}", "",
             f"Blocks: {json.dumps(m['arm_layers'])}; items {m['items']['items']} ({m['items']['entities']} bridge "
             f"entities), the control's source before the bridge in {m['items']['control_before_bridge']}", ""]  # fmt: skip
    for w in X.READERS:
        r = nums[w]
        lines.append(f"{'lookup' if w == X.LOOKUP else 'recall (beside)'}: n {r['n']}, S_whole {fmt(r['S']['none'])} "
                     f"({r['switched']['none']} switched; X0-valid {r['x0_valid']}), clean answer kept with no block "
                     f"{fmt(r['clean_kept']['none'])}")  # fmt: skip
        for a in ARMS[1:]:
            lines.append(f"  {ARM_TEXT[a]}: S {fmt(r['S'][a])}, cut {fmt(r['cut'][a], r['cut_ci'][a])}, clean kept "
                         f"{fmt(r['clean_kept'][a])}, edges (median) {r['edges_median'][a]:.0f}")  # fmt: skip
    lines += ["", f"Whole change vs the conflict run's stored switch (descriptive): {json.dumps(agree)}", "",
              *example_lines(rows, items)]  # fmt: skip
    blob = {"prediction": NO_PREDICTION, "rule": RULE, "as_computed": AS_COMPUTED, "run": name, "layer": m["layer"],
            "arm_layers": m["arm_layers"], "label": res, "readers": {("lookup" if w == X.LOOKUP else "recall"): v
            for w, v in nums.items()}, "agreement": agree, "status": "UNVERIFIED"}  # fmt: skip
    (out / "verdict.json").write_text(json.dumps(blob, indent=1, default=float) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", default=RUN)
    ap.add_argument("--why", default="53.4, Dan 29 Oct ~10:05 (lightning_attn_block): does the lookup read the "
                    "bridge word through attention blocks 19 and 26? Rule fixed then, no prediction")  # fmt: skip
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        stage_run(a.name, a.why)
    else:
        stage_verdict(a.name)


if __name__ == "__main__":
    main()
