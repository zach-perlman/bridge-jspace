"""x45p (batch 45, test 45p; jobs/c3/batch45.yaml, design, rule and readings fixed in advance; Q45.13 in
predictions/2026-10-26_dan.md): when its locker came first, does the recall read the new item's earlier mention?

Scenes: each model's 45m run (x0_necessity --alt fresh: one locker item that nobody picks is added to both prompts and
the asked pick changes from the bridge to it; only the bridge token differs), its eligible scenes at the layer fixed in
advance (the scenes of its chat outcomes at L), kept where the new item's (alt) locker sentence comes before the asked
pick (x0_strata's 'alt locker vs asked pick' == before). That sentence is in O too: it is the inserted locker sentence,
in both prompts. The cases are rebuilt with X.build_cases (alt fresh, chat) and must equal the run's cases.jsonl.

O = the original prompt, S = the changed one. Every edit at L = X.PREDICTED (45m's layer), on O, one read per arm:
  none   O unedited
  whole  h_S - h_O added at the bridge word (45m's whole arm, rerun; a check against its stored outcome)
  a1     the base edit: the whole change minus its J++ part (signed OMP, k = 25, over the J++ lens atoms at L as X0
         takes them: X.fit(jdic, x, 25, "signed"), jdic = JLens(model, "jpp").vectors(L, letter tokens)); 45m's no_part
  a2     a1, and at the new item's token(s) in its locker sentence -J++(h): that token's state h becomes h minus its own
         J++ part (signed OMP, k = 25, on h itself)
  a3     a1, and at the same tokens h minus a random part of the same share of ||h||^2 (X0's random subspace, seed
         888 + L: statement_positions.random_basis / random_subspace_part)
  a4     a1, and a2's edit at the item token(s) of another locker sentence: the first in context order whose item is
         neither the bridge nor the new item (the control)
  o2     a2's item edit alone, no base edit (O's own reads must stay right; reported, not in the rule)
The item tokens: the tokens whose characters overlap the item's name inside its locker sentence of the rendered prompt
('The locker of [the] <item> is <n>.'; offsets of the rendered prompt). h is O's clean state at L: an edit acts on a
block's output at its own positions only, so the base edit at the bridge word leaves every other position's state at L
as it was. Reads: X0's chat read (the prompt with a digit's space token appended), both readers; switch = the top token
is S's answer's first token; right = the top token is O's.

Rule (stage verdict; recall reader, point estimates): loss_k = 1 - S_k / S_1 over the items, S_k the recall's switch
rate under arm k. A model holds if loss_2 - loss_3 >= 0.2 and loss_2 - loss_4 >= 0.15 (EPS 1e-9); a model whose base
edit switches fewer than 30 recalls is not tested (and does not hold). The batch holds if at least 2 of the 3 models
hold. Cluster-bootstrap CIs over the bridge items (X0's entity clusters, 10,000 resamples, seed 0) beside the points;
the lookup reported beside it; O alone with a2's edit: the share of items both readers still read right.

SEALED: the run writes no verdict. The verdict stage refuses until predictions/2026-10-26_dan.md holds Dan's Q45.13
answer at the committed HEAD.

uv run python scripts/x45p.py plan                                                       # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x45p.py run --name qwen35_9b_x45p             # GPU (sealed)
uv run python scripts/x45p.py verdict --runs qwen35_9b_x45p x45p_27b muse30b_x45p        # CPU, after Dan's Q45.13
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x0_strata as ST
from scripts import x45b_binding as B

EXP = "x45p"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch45.yaml"
PREDICTIONS = "predictions/2026-10-26_dan.md"
QUESTION = "Q45.13"
RUN_45M = {"qwen3.5-9b": "qwen35_9b_x45m_fresh", "qwen3.6-27b": "x45m_fresh_27b",
           "muse-glimmer-30b": "muse30b_x45m_fresh"}  # fmt: skip
RUNS = {"qwen3.5-9b": "qwen35_9b_x45p", "qwen3.6-27b": "x45p_27b", "muse-glimmer-30b": "muse30b_x45p"}
# the 122B's coverage (Dan 18:20, jobs/c3/batch53.yaml coverage_122b_1820 item 6): its 45m run, kept out of RUN_45M so
# 45p's own verdict (three models) is unchanged; verdict --coverage reads such runs alone
COVERAGE_45M = {"qwen3.5-122b-a10b": "qwen35_122b_x45m_fresh"}
NO_PREDICTION = "no prediction: coverage run on an already-scored rule"
RENDERING = "chat"
ARMS = ("none", "whole", "a1", "a2", "a3", "a4", "o2")
ARM_TEXT = {
    "none": "O unedited",
    "whole": "the whole change at the bridge word (45m's whole arm, rerun)",
    "a1": "(1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word",
    "a2": "(2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part",
    "a3": "(3) the base edit, and the same tokens without a random part of the same share",
    "a4": "(4) the base edit, and the control item's token(s) without their own J++ part",
    "o2": "O alone with (2)'s item edit (no base edit)",
}
LOSS_ARMS = ("a2", "a3", "a4")
MARGIN_3, MARGIN_4, MIN_SWITCHES, MODELS_MIN = 0.2, 0.15, 30, 2
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULE = ("the recall reads the earlier mention if the recall's switch loss in (2) exceeds (3) by at least 0.2 and (4) by "
        "at least 0.15 (loss_k = 1 - S_k / S_1, point estimates), on at least 2 of 3 models; a model whose base edit "
        "switches fewer than 30 recalls is not tested")  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


# ---- positions (tokenizer only) -----------------------------------------------------------------------------------


class NoControl(ValueError):
    """No locker sentence names an item other than the bridge and the new item."""


def locker_items(context: str) -> list[tuple[str, str]]:
    """Each locker sentence of the context in order, with its item ('The locker of [the] <item> is <n>.')."""
    out = []
    for s in B.locker_sentences(context):
        m = B.LOCKER_RE.match(s)
        assert m, f"{s!r} is not a locker sentence"
        out.append((s, m.group(1)))
    return out


def item_spans(text: str, context: str, bridge: str, new: str) -> dict[str, dict]:
    """In the rendered prompt `text`, the character span of the new item's name inside its locker sentence and of the
    control item's: the item of the first locker sentence in context order that is neither the bridge nor the new item.
    Raises NoControl if there is none."""
    assert text.count(context) == 1, "the context is not once in the prompt"
    lockers = locker_items(context)
    spans = B.locker_spans(text, context)  # [start, end) of each locker sentence in the prompt, in context order

    def at(k: int) -> dict:
        sent, item = lockers[k]
        i = spans[k][0] + B.LOCKER_RE.match(sent).span(1)[0]  # type: ignore[union-attr]
        return {"item": item, "sentence": sent, "index": k, "span": [i, i + len(item)]}

    mine = [k for k, (_, item) in enumerate(lockers) if item == new]
    assert len(mine) == 1, f"the new item {new!r} has {len(mine)} locker sentences"
    ctl = next((k for k, (_, item) in enumerate(lockers) if item not in (bridge, new)), None)
    if ctl is None:
        raise NoControl("no locker item other than the bridge and the new item")
    return {"new": at(mine[0]), "control": at(ctl)}


def token_positions(offsets: list[tuple[int, int]], span: list[int]) -> list[int]:
    """The token positions whose characters overlap the span (statement_positions.tokens_in)."""
    from scripts import statement_positions as SP

    out = SP.tokens_in(offsets, span[0], span[1])
    assert out, f"no token overlaps {span}"
    return out


def exact(tok, ids: list[int], positions: list[int], name: str) -> bool:
    """The tokens at `positions` decode to the name and nothing else (whitespace aside)."""
    return tok.decode([ids[p] for p in positions]).strip() == name


def marked(text: str, spans: list[tuple[int, int, str]]) -> str:
    """The text with ⟦label:…⟧ around each span (no overlaps); a span's leading whitespace stays outside."""
    out, last = [], 0
    for a, b, label in sorted(spans):
        while a < b and text[a].isspace():
            a += 1
        assert a >= last, f"span ({a}, {b}) overlaps the previous one"
        out += [text[last:a], f"⟦{label}:", text[a:b], "⟧"]
        last = b
    out.append(text[last:])
    return "".join(out)


# ---- items (tokenizer only) ---------------------------------------------------------------------------------------


def stored_reads(src: Path, layer: int) -> tuple[list[str], dict[str, dict]]:
    """The 45m run's items at the layer (its chat outcomes' scenes, in order) and, per scene and reader, its stored
    whole and no_part (J++ k = 25 signed) switches: the checks for this run's whole and a1."""
    scenes: dict[str, None] = {}
    stored: dict[str, dict] = collections.defaultdict(lambda: {"whole": {}, "a1": {}})
    for r in X.read_jsonl(src / "outcomes.jsonl"):
        if r["rendering"] != RENDERING or r["layer"] != layer:
            continue
        if r["arm"] == "whole":
            if r["reader"] == X.LOOKUP:
                scenes.setdefault(r["scene"])
            stored[r["scene"]]["whole"][r["reader"]] = r["switched"]
        elif r["arm"] == "no_part" and (r["dict"], r["k"], r["omp"]) == X.MAIN:
            stored[r["scene"]]["a1"][r["reader"]] = r["switched"]
    return list(scenes), {s: stored[s] for s in scenes}


def rebuild(tok, set_name: str) -> list[dict]:
    """45m's cases (x0_necessity alt fresh, chat), rebuilt on this tokenizer; X0's module settings restored after."""
    old = X.ALT, X.RENDERINGS
    X.ALT, X.RENDERINGS = "fresh", (RENDERING,)
    try:
        cases, _ = X.build_cases(tok, set_name)
    finally:
        X.ALT, X.RENDERINGS = old
    return cases


def select(tok, run_45m: str, layer: int) -> tuple[list[dict], dict]:
    """The 45p items in the 45m run's scene order (the new item's locker sentence before the asked pick, a control
    locker item, every patched token exactly its item's name) and the counts: the run's items, the order split, drops
    by reason, token counts, where the control sits."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import tasks_v2 as T

    src = X.RESULTS / run_45m
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt") == "fresh", f"{run_45m}: alt {m.get('alt')!r}, not 45m's fresh alt"
    assert m["predicted"] == layer, f"{run_45m}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{run_45m} is a {m['model']['target']} run, not {pins.TARGET}'s"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run_45m}"
    scenes, stored = stored_reads(src, layer)
    assert scenes, f"{run_45m}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    rebuilt = {c["scene"]: c for c in rebuild(tok, m["set"])}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, dropped = [], collections.Counter()
    order, n_tok, ctl_where = collections.Counter(), collections.Counter(), collections.Counter()
    for scene in scenes:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run_45m}"
        assert c["fresh"] == old[scene]["fresh"], f"{scene}: the inserted item changed since {run_45m}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        feats = ST.features(c)
        order[feats["alt locker vs asked pick"]] += 1
        if feats["alt locker vs asked pick"] != "before":
            continue
        if not B.same_after_bridge(c):
            dropped["O and S differ beyond the bridge word"] += 1
            continue
        texts, offsets = {}, {}
        for w in X.READERS:
            rd = c["readers"][w]
            texts[w] = X.render(tok, by_id[rd["id"]], RENDERING, c["context"])
            enc = raw_encoding(tok, texts[w], offsets=True)
            assert enc["input_ids"] == rd["ids"]["org"], f"{scene} {w}: the rendered prompt's ids differ"
            offsets[w] = enc["offset_mapping"]
        lk = X.LOOKUP
        ids = c["readers"][lk]["ids"]["org"]
        try:
            spans = item_spans(texts[lk], c["context"], c["bridge"], c["cf_bridge"])
        except NoControl:
            dropped["no locker item other than the bridge and the new item"] += 1
            continue
        new, ctl = spans["new"], spans["control"]
        assert new["item"] == c["fresh"]["item"], f"{scene}: the new item is not 45m's"
        assert new["sentence"] == c["fresh"]["sentence"], f"{scene}: the new item's sentence is not 45m's"
        new["positions"] = token_positions(offsets[lk], new["span"])
        ctl["positions"] = token_positions(offsets[lk], ctl["span"])
        if not exact(tok, ids, new["positions"], new["item"]):
            dropped["the new item's tokens are not exactly its name"] += 1
            continue
        if not exact(tok, ids, ctl["positions"], ctl["item"]):
            dropped["the control item's tokens are not exactly its name"] += 1
            continue
        patched = [c["pos"], *new["positions"], *ctl["positions"]]
        assert len(set(patched)) == len(patched), f"{scene}: patched positions overlap"
        assert max(new["positions"]) < c["pos"], f"{scene}: the new item's locker tokens are not before the bridge"
        if c["readers"][X.RECALL]["ids"]["org"][: max(patched) + 1] != ids[: max(patched) + 1]:
            dropped["the readers' prompts differ before the last patched token"] += 1
            continue
        ctl["vs_asked_pick"] = "before" if max(ctl["positions"]) < c["pos"] else "after"
        ctl["vs_new"] = "before" if ctl["index"] < new["index"] else "after"
        for part in (new, ctl):
            part["text"] = tok.decode([ids[p] for p in part["positions"]])
        n_tok[f"new {len(new['positions'])}, control {len(ctl['positions'])}"] += 1
        ctl_where[f"{ctl['vs_new']} the new item, {ctl['vs_asked_pick']} the asked pick"] += 1
        o_off = offsets[lk]
        out.append({
            "scene": scene, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
            "upstream": c["upstream"], "features": feats, "pos": c["pos"], "space": c["space"],
            "read_suffix": tok.decode(c["space"]), "context": c["context"], "cf_context": c["cf_context"],
            "fresh": c["fresh"], "new": new, "control": ctl,
            "marks": {"bridge": [list(o_off[c["pos"]])],
                      "new": [list(s) for s in B.merged_spans(o_off, new["positions"])],
                      "control": [list(s) for s in B.merged_spans(o_off, ctl["positions"])]},
            "readers": {w: {**{k: c["readers"][w][k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b",
                                                             "ids")}, "text": {"org": texts[w]}} for w in X.READERS},
            "stored": stored[scene],
        })  # fmt: skip
    counts = {"run_45m": run_45m, "layer": layer, "items_at_L": len(scenes),
              "alt locker vs asked pick": dict(order), "dropped": dict(dropped), "items": len(out),
              "entities": len({it["entity"] for it in out}), "tokens": dict(n_tok), "control": dict(ctl_where)}  # fmt: skip
    return out, counts


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    """The example items: k random indices of n (seed 0), as X0 picks its examples."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def item_marked(it: dict, reader: str) -> str:
    """The reader's O prompt as the model reads it (the digit's space token appended), the bridge word, the new item's
    and the control item's patched tokens marked."""
    spans = [(a, b, role) for role in ("bridge", "new", "control") for a, b in it["marks"][role]]
    return marked(it["readers"][reader]["text"]["org"] + it["read_suffix"], spans)


def stage_plan() -> dict:
    """Tokenizer only: the target's items, drops and positions, and one example (seed 0) with the patches marked."""
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = select(tok, {**RUN_45M, **COVERAGE_45M}[pins.TARGET], layer)
    counts["target"] = pins.TARGET
    if items:
        it = items[example_indices(len(items), 1)[0]]
        counts["example"] = {
            "scene": it["scene"], "bridge": it["entity"], "new": it["new"]["item"], "control": it["control"]["item"],
            "new_tokens": {p: tok.decode([it["readers"][X.LOOKUP]["ids"]["org"][p]]) for p in it["new"]["positions"]},
            "control_tokens": {p: tok.decode([it["readers"][X.LOOKUP]["ids"]["org"][p]])
                               for p in it["control"]["positions"]},
            "bridge_token": {it["pos"]: tok.decode([it["readers"][X.LOOKUP]["ids"]["org"][it["pos"]]])},
            "lookup_O_marked": item_marked(it, X.LOOKUP)}  # fmt: skip
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    return counts


# ---- GPU ----------------------------------------------------------------------------------------------------------


def jpp_and_random(x, jdic, basis, k: int = X.K_MAIN):
    """Per row of x [n, d]: its J++ part (signed OMP, k atoms of jdic; X.fit as X0) and a random part of the same share
    of the row's squared norm (X0's random subspace), and that share; a zero row keeps zero parts."""
    import torch

    from scripts import statement_positions as SP

    x = x.float()
    part = torch.zeros_like(x)
    live = x.norm(dim=-1) > 0
    if bool(live.any()):
        part[live] = X.fit(jdic, x[live], k, "signed").float()
    share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    return part, SP.random_subspace_part(x, share, basis).float(), share


def edit_sets(add_rows, layer: int, pos: int, whole, base, new_pos: list[int], new_part, new_rand,
              ctl_pos: list[int], ctl_part) -> dict[str, dict]:  # fmt: skip
    """Each arm's edit set ({layer: add_rows(rows [P, d], positions)}), in ARMS order. whole and base are [d] rows at the
    bridge word; new_part / new_rand / ctl_part are the item tokens' parts [P, d], subtracted."""
    import torch

    def at(rows: list, positions: list[int]) -> dict:
        return {layer: add_rows(torch.cat([r if r.dim() == 2 else r[None] for r in rows]), positions)}

    out = {"none": {}, "whole": at([whole], [pos]), "a1": at([base], [pos]),
           "a2": at([base, -new_part], [pos, *new_pos]), "a3": at([base, -new_rand], [pos, *new_pos]),
           "a4": at([base, -ctl_part], [pos, *ctl_pos]), "o2": at([-new_part], list(new_pos))}  # fmt: skip
    assert tuple(out) == ARMS
    return out


def stage_run(name: str, why: str, below: bool = False) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "45p renders 45m's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert below or target in RUN_45M, f"45p runs on {sorted(RUN_45M)}, not {target}"
    run_45m, layer = (B.fresh_of(target, True) if below else {**RUN_45M, **COVERAGE_45M}[target]), X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / run_45m
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "45p",
         "spec": "jobs/c3/batch45.yaml (45p)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, src / "manifest.json", src / "cases.jsonl", src / "outcomes.jsonl")},
         "run_45m": run_45m, "layer": layer, "arms": ARM_TEXT, "k": X.K_MAIN, "omp": "signed",
         "random_part": f"X0's random subspace, seed {X.SUBSPACE_SEED} + layer, at each token's J++ share of ||h||^2",
         "items_rule": "the 45m run's items at L (chat) whose new item's (alt) locker sentence comes before the asked "
                       "pick (x0_strata); O and S the same but for the bridge word; a control locker item; every "
                       "patched token exactly its item's name; else dropped and counted",
         "positions": "the tokens overlapping the item's name inside its locker sentence (character offsets of the "
                      "rendered prompt); control: the first locker sentence in context order whose item is neither the "
                      "bridge nor the new item",
         "h": "O's clean state at L (an edit at L changes only its own positions' states at L)",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = top token is S's answer; "
                 "right = top token is O's", "rule": RULE, "decisive_reader": X.RECALL,
         "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED, "random_subspace": f"{X.SUBSPACE_SEED} + layer",
                   "fresh_draws": X.FRESH_SEED}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    if below:  # batch 52, Dan's morning queue item 1: below gate, exploratory
        m |= {"question": B.BELOW_GATE, "below_gate": {"note": B.BELOW_GATE, "source_gate": B.source_gate(run_45m)},
              "sealed": "none (below gate, exploratory): verdict --below-gate"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    model = load_model()
    tok = model.tokenizer
    items, counts = select(tok, run_45m, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
    examples = set(example_indices(len(items)))
    rows, norms, greedy, basis = [], [], [], None
    with torch.no_grad():
        for i, it in enumerate(progress(items, f"45p at L{layer} (item)")):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer]
                 for v in ("org", "alt")}  # fmt: skip
            pos, new_pos, ctl_pos = it["pos"], it["new"]["positions"], it["control"]["positions"]
            whole = (h["alt"][pos] - h["org"][pos]).float().to(jdic.device)[None]
            if basis is None:
                basis = SP.random_basis(whole.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer))
                basis = basis.to(jdic.device)
            h_new = h["org"][new_pos].float().to(jdic.device)
            h_ctl = h["org"][ctl_pos].float().to(jdic.device)
            w_part, _, w_share = jpp_and_random(whole, jdic, basis)
            n_part, n_rand, n_share = jpp_and_random(h_new, jdic, basis)
            c_part, _, c_share = jpp_and_random(h_ctl, jdic, basis)
            edits = edit_sets(AddRows, layer, pos, whole[0], whole[0] - w_part[0], new_pos, n_part, n_rand, ctl_pos,
                              c_part)  # fmt: skip
            n_rand_share = n_rand.norm(dim=-1) ** 2 / (h_new.norm(dim=-1) ** 2).clamp_min(1e-30)
            rounded = lambda t, nd: [round(float(x), nd) for x in t]  # noqa: E731
            norms.append({"scene": it["scene"], "whole_norm": round(float(whole.norm()), 4),
                          "whole_jpp_share": round(float(w_share[0]), 5),
                          "new_h_norm": rounded(h_new.norm(dim=-1), 4), "new_jpp_share": rounded(n_share, 5),
                          "new_rand_share": rounded(n_rand_share, 5), "control_h_norm": rounded(h_ctl.norm(dim=-1), 4),
                          "control_jpp_share": rounded(c_share, 5)})  # fmt: skip
            for w, rd in it["readers"].items():
                base_row = {"scene": it["scene"], "entity": it["entity"], "domain": it["domain"], "reader": w}
                logits, _ = X.read_logits(model, rd["ids"]["org"], list(edits.values()), RENDERING, it["space"], ws)
                for arm, lg in zip(edits, logits, strict=True):
                    top = int(lg.argmax())
                    rows.append({**base_row, "arm": arm, **X.read_row(lg, rd, digits), "right": int(top == rd["tok_A"]),
                                 "top_text": tok.decode([top])})  # fmt: skip
                if i in examples:
                    o_ids = torch.tensor([rd["ids"]["org"]], device=model.device)
                    texts = model.generate_batch(o_ids, X.GEN_TOKENS, list(edits.values()))
                    greedy += [{"scene": it["scene"], "reader": w, "arm": arm, "greedy": t}
                               for arm, t in zip(edits, texts, strict=True)]  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print("wrote", out, "(sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU) ------------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q45.13 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    m = re.search(r"^Dan:(.*)$", block, re.M)
    return m.group(1).strip() if m else ""


def item_table(rows: list[dict], reader: str) -> tuple[list[str], list[str], dict[str, list[int]]]:
    """One reader's items (in row order), their bridge entities, and each arm's 0/1 switch per item; every item must
    have every arm."""
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["switched"])
    scenes = list(entity)
    missing = [(s, a) for s in scenes for a in ARMS if (s, a) not in by]
    assert not missing, f"{reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    return scenes, [entity[s] for s in scenes], {a: [by[(s, a)] for s in scenes] for a in ARMS}


def numbers(switched: dict[str, list[int]], entities: list[str], n_boot: int = X.N_BOOT,
            seed: int = X.BOOT_SEED) -> dict[str, Any]:  # fmt: skip
    """Each arm's switch rate, loss_k = 1 - S_k / S_1 for k = 2, 3, 4, and loss_2 - loss_3, loss_2 - loss_4, with 95%
    percentile CIs from X0's cluster bootstrap over the bridge entities (the same draws for every arm: paired). Points
    from counts; a loss is nan when arm 1 switches nothing."""
    n = len(entities)
    hits = {a: int(sum(switched[a])) for a in ARMS}
    boot = X.resampled_rates(switched, entities, n_boot, seed)
    loss_b = {a: X.dependence(boot["a1"], boot[a]) for a in LOSS_ARMS}
    h1 = hits["a1"]
    loss = {a: (1 - hits[a] / h1) if h1 else math.nan for a in LOSS_ARMS}
    return {"n": n, "entities": len(set(entities)), "hits": hits,
            "rate": {a: [hits[a] / n, *X.interval(boot[a])] for a in ARMS},
            "loss": {a: [loss[a], *X.interval(loss_b[a])] for a in LOSS_ARMS},
            "diff": {"2-3": [loss["a2"] - loss["a3"], *X.interval(loss_b["a2"] - loss_b["a3"])],
                     "2-4": [loss["a2"] - loss["a4"], *X.interval(loss_b["a2"] - loss_b["a4"])]}}  # fmt: skip


def rule(recall: dict[str, Any]) -> dict[str, Any]:
    """45p on one model's recall numbers (point estimates): not tested under MIN_SWITCHES base-edit switches; else
    holds iff loss_2 - loss_3 >= 0.2 and loss_2 - loss_4 >= 0.15 (EPS)."""
    h1 = recall["hits"]["a1"]
    if h1 < MIN_SWITCHES:
        return {"status": "not tested", "holds": False,
                "why": f"the base edit switches {h1} recalls, fewer than {MIN_SWITCHES}"}  # fmt: skip
    d3, d4 = recall["diff"]["2-3"][0], recall["diff"]["2-4"][0]
    ok3, ok4 = d3 >= MARGIN_3 - EPS, d4 >= MARGIN_4 - EPS
    why = (f"loss_2 - loss_3 = {d3:.3f} {'>=' if ok3 else '<'} {MARGIN_3}; loss_2 - loss_4 = {d4:.3f} "
           f"{'>=' if ok4 else '<'} {MARGIN_4} (base-edit recall switches {h1})")  # fmt: skip
    return {"status": "tested", "holds": ok3 and ok4, "over_random": ok3, "over_control": ok4, "why": why}


def o_alone(rows: list[dict]) -> dict[str, Any]:
    """O alone with a2's item edit (and O unedited beside it): per arm the share of items each reader reads right (top
    token = O's answer) and the share both readers read right."""
    out: dict[str, Any] = {}
    for arm in ("none", "o2"):
        right: dict[str, dict[str, int]] = collections.defaultdict(dict)
        for r in rows:
            if r["arm"] == arm:
                right[r["scene"]][r["reader"]] = int(r["right"])
        n = len(right)
        both = sum(all(v.get(w, 0) for w in X.READERS) for v in right.values())
        out[arm] = {"n": n, "both_right": both, "both_right_share": both / n if n else None,
                    **{f"{READER_NAME[w]}_right": sum(v.get(w, 0) for v in right.values()) for w in X.READERS}}  # fmt: skip
    return out


def agreement(items: list[dict], rows: list[dict]) -> dict[str, Any]:
    """Descriptive checks against the 45m run: the rerun whole and a1 arms against its stored whole and no_part."""
    by = {(r["scene"], r["reader"], r["arm"]): int(r["switched"]) for r in rows}
    out = {}
    for w in X.READERS:
        for arm in ("whole", "a1"):
            pairs = [(by[(it["scene"], w, arm)], it["stored"][arm][w]) for it in items if w in it["stored"][arm]]
            out[f"{READER_NAME[w]} {arm} vs 45m's stored {'whole' if arm == 'whole' else 'no_part'}"] = {
                "n": len(pairs), "agree": sum(a == b for a, b in pairs), "rerun": sum(a for a, _ in pairs),
                "stored": sum(b for _, b in pairs)}  # fmt: skip
    return out


def median(xs: list[float]) -> float | None:
    return round(statistics.median(xs), 5) if xs else None


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One model's run: pending (not here / no outcomes), or its numbers per reader and the rule on the recall."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run) or ("nemotron-3.5-lightning" if "_below" in run else None)
        assert target, f"no 45p run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {"run": run, "target": target, "status": "pending", "holds": False,
                "why": "the run has no manifest or outcomes here"}  # fmt: skip
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    items = X.read_jsonl(src / "cases.jsonl")
    readers = {}
    for w in X.READERS:
        _, entities, switched = item_table(rows, w)
        readers[READER_NAME[w]] = numbers(switched, entities, n_boot)
    r = rule(readers["recall"])
    norms = X.read_jsonl(src / "norms.jsonl")
    shares = {"whole_jpp_share": median([x["whole_jpp_share"] for x in norms]),
              "new_jpp_share": median([s for x in norms for s in x["new_jpp_share"]]),
              "new_rand_share": median([s for x in norms for s in x["new_rand_share"]]),
              "control_jpp_share": median([s for x in norms for s in x["control_jpp_share"]])}  # fmt: skip
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "run_45m": m["run_45m"],
            **r, "readers": readers, "o_alone": o_alone(rows), "checks": agreement(items, rows),
            "shares_median": shares, "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def batch_verdict(models: list[dict]) -> dict[str, Any]:
    """The rule over the models: holds once MODELS_MIN hold; does not hold once too few can still hold; else pending."""
    n_hold = sum(bool(m["holds"]) for m in models)
    n_pending = sum(m["status"] == "pending" for m in models)
    label = "holds" if n_hold >= MODELS_MIN else "does not hold" if n_hold + n_pending < MODELS_MIN else "pending"
    answer = {"holds": "(a) yes", "does not hold": "(b) no"}.get(label, "pending")
    return {"label": label, QUESTION: answer, "models_holding": n_hold, "models": len(models),
            "tested": [m["run"] for m in models if m["status"] == "tested"],
            "not_tested": [m["run"] for m in models if m["status"] == "not tested"],
            "pending": [m["run"] for m in models if m["status"] == "pending"]}  # fmt: skip


def fmt(v: list) -> str:
    return "-" if v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])) else (
        f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]".replace("-", "−"))  # fmt: skip


def example_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items of the run (seed 0): each reader's O prompt with the patches marked, each arm's top token and
    greedy text."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {run}: {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        it = items[i]
        lines += [f"### {it['scene']} ({it['domain']}): bridge {it['entity']} → {it['cf_bridge']}; control "
                  f"{it['control']['item']} ({it['control']['vs_asked_pick']} the asked pick)", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "",
                      "```", item_marked(it, w), "```", "", "| arm | what | top token | switched | right | greedy |",
                      "|---|---|---|---|---|---|"]  # fmt: skip
            for arm in ARMS:
                r = reads[(it["scene"], w, arm)]
                lines.append(f"| {arm} | {ARM_TEXT[arm]} | {r['top_text']!r} | {r['switched']} | {r['right']} | "
                             f"{greedy.get((it['scene'], w, arm))!r} |")  # fmt: skip
            lines.append("")
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT, below: bool = False, coverage: bool = False) -> Path:
    """45p's verdict (sealed until Q45.13), or with below (batch 52, Dan's morning queue item 1) the below-gate runs
    alone: the rule per model, no batch count, no seal, written to x52_45p_below-<UTC>/."""
    answer = B.BELOW_GATE if below else NO_PREDICTION if coverage else dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    known = set(B.FRESH_BELOW) if below else set(COVERAGE_45M) if coverage else set(RUN_45M)
    assert set(targets) <= known, f"45p runs on {sorted(known)}, not {sorted(set(targets) - known)}"
    if not below and not coverage:
        models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "holds": False, "why": "no run given"}
                   for t in RUN_45M if t not in targets]  # fmt: skip
    v = batch_verdict(models)
    stem = "x52_45p_below" if below else "x53_45p_coverage" if coverage else "x45p"
    out = RESULTS / f"{stem}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 45p: does the recall read the item's earlier mention when its locker came first?", "",
             f"Batch 45, test 45p (jobs/c3/batch45.yaml; {QUESTION}, Dan: {answer}). 45m's scenes (only the bridge "
             "token differs) whose new item's locker sentence comes before the asked pick; every edit at the layer "
             "fixed in advance, on O. loss_k = 1 − S_k / S_1 over the items, S_k the recall's switch rate under arm k; "
             f"cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}.", "",
             f"**Verdict: {v['label']}** ({QUESTION} {v[QUESTION]}): {v['models_holding']} of {v['models']} models "
             f"hold (at least {MODELS_MIN} needed)"
             + (f"; not tested: {', '.join(v['not_tested'])}" if v["not_tested"] else "")
             + (f"; pending: {', '.join(v['pending'])}" if v["pending"] else "") + ".", "",
             "| model | run | status | n | recall S_1 (switches) | loss_2 − loss_3 | loss_2 − loss_4 | holds |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m.get('target', '-')} | {m['run']} | pending ({m['why']}) | | | | | |")
            continue
        rc = m["readers"]["recall"]
        lines.append(f"| {m['target']} | {m['run']} | {m['status']} | {rc['n']} | {fmt(rc['rate']['a1'])} "
                     f"({rc['hits']['a1']}) | {fmt(rc['diff']['2-3'])} | {fmt(rc['diff']['2-4'])} | "
                     f"{'yes' if m['holds'] else 'no'} |")  # fmt: skip
    lines += ["", "Per reader (the recall decides; the lookup reported beside it): switch rate per arm, and loss_k.", "",
              "| model | reader | " + " | ".join(ARMS) + " | loss_2 | loss_3 | loss_4 |",
              "|---|---|" + "---|" * (len(ARMS) + 3)]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for w in ("recall", "lookup"):
            r = m["readers"][w]
            lines.append(f"| {m['target']} | {w} | " + " | ".join(fmt(r["rate"][a]) for a in ARMS) + " | "
                         + " | ".join(fmt(r["loss"][a]) for a in LOSS_ARMS) + " |")  # fmt: skip
    lines += ["", "Arms: " + "; ".join(f"{a} = {t}" for a, t in ARM_TEXT.items()) + ".", "",
              "O alone with (2)'s item edit (reported, not in the rule): items both readers still read right (O's own "
              "answers), against O unedited.", "", "| model | o2: both right | o2: lookup / recall right | none: both "
              "right |", "|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        o, nn = m["o_alone"]["o2"], m["o_alone"]["none"]
        lines.append(f"| {m['target']} | {o['both_right']} / {o['n']} ({o['both_right_share']:.2f}) | "
                     f"{o['lookup_right']} / {o['recall_right']} | {nn['both_right']} / {nn['n']} |")  # fmt: skip
    lines += ["", "Items, shares and checks (descriptive):", ""]
    for m in models:
        if m["status"] == "pending":
            continue
        p = m["plan"]
        lines.append(f"- {m['target']} ({m['run']}, from {m['run_45m']}, L{m['layer']}): {p['items']} items of "
                     f"{p['items_at_L']} at L (alt locker {p['alt locker vs asked pick']}; dropped {p['dropped'] or 'none'};"
                     f" tokens {p['tokens']}; control {p['control']}); median J++ share: the bridge-word change "
                     f"{m['shares_median']['whole_jpp_share']}, the new item's h {m['shares_median']['new_jpp_share']} "
                     f"(random part {m['shares_median']['new_rand_share']}), the control's h "
                     f"{m['shares_median']['control_jpp_share']}; checks: " + "; ".join(
                         f"{k}: {c['agree']} of {c['n']} agree (rerun {c['rerun']}, stored {c['stored']})"
                         for k, c in m["checks"].items()))  # fmt: skip
    if below:
        lines = [ln.replace(f"{QUESTION}, Dan: ", "batch 52 below gate, ") for ln in lines]
        lines.insert(2, "The batch line counts the given runs only (Lightning alone): not a re-score of 45p's 2 of 3.")
        lines.insert(3, "")
    (out / "x45p.json").write_text(json.dumps({"runs": runs, "dan": answer, "verdict": v, "models": models}, indent=1)
                                   + "\n")  # fmt: skip
    (out / "x45p.md").write_text("\n".join(lines) + "\n")
    ex = ["# 45p examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, "
          "⟦new:…⟧ the new item's patched token(s), ⟦control:…⟧ the control item's. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x45p/<name>/)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict: the 45p runs (9B, 27B, Muse)")
    ap.add_argument("--why", default="batch 45, test 45p (jobs/c3/batch45.yaml; Q45.13)")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--below-gate", action="store_true",
                    help="run / verdict: batch 52, Lightning's clean design below its gate (exploratory)")  # fmt: skip
    ap.add_argument("--coverage", action="store_true",
                    help=f"verdict: coverage runs (COVERAGE_45M's models) alone, '{NO_PREDICTION}'")  # fmt: skip
    a = ap.parse_args()
    assert not (a.coverage and a.below_gate), "--coverage and --below-gate are separate verdicts"
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why, a.below_gate)
    else:
        stage_verdict(a.runs, a.n_boot, a.below_gate, a.coverage)


if __name__ == "__main__":
    main()
