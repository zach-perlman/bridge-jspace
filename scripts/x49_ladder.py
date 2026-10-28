"""x49_ladder (batch 49, test 49.2; jobs/c3/batch49.yaml with amendment 2's 49.2 item, design and rules fixed in
advance; Q49.2 in predictions/2026-10-28_dan.md): the removal ladder. 47.5 took the J++ part out at one token and one
layer and the recall kept 0.97; Zach's knock-out takes the top-10 lens directions out at every token over a band and
the recall breaks. Where between the two does "follows" become "needs", and does the lookup ever need it?

Scenes: the clean design (45m, x0_necessity --alt fresh: a locker item nobody picks becomes S's asked pick; only the
bridge token differs), each model's 45m run, its eligible scenes at the layer fixed in advance (the scenes of its chat
outcomes at L; the run's gate passed), rebuilt with X.build_cases and equal to its cases.jsonl. Order: x0_strata's 'alt
locker vs asked pick' (x45p's split): locker-first = the new item's locker sentence (its earlier mention) comes before
the asked pick, locker-after = after (no earlier mention); x45m's both-lockers group is kept beside, per item.

On S (the changed prompt), read by X0's chat read (the prompt with a digit's space token appended; kept = the top token
is S's answer's first token), both readers. The removal is 47.5's zeroing (x47_zero): at layer l the state minus its
projection on the span of the 25 signed-OMP atoms of Δ_l = h_S - h_O at the bridge word over the J++ lens's letter-token
atoms at l (per-layer lens and OMP; X0's picks), on the state as it arrives. Amendment 2: at tokens other than the
bridge word the removal is the projection of that token's state onto the span of the same 25 atoms (the bridge item's
lens identity wherever it appears). Rungs, each beside a random subspace of the same share per token (the first k
columns of X0's random basis, seed 888 + l, k per token so they hold the atoms' share of that token's ||h_S||^2 on S's
clean state at l: statement_positions.random_subspace_part's rule):
  1  the bridge word, at L                                  (47.5's zero_L)
  2  the bridge word, at L..L+3                             (47.5's zero_L3)
  3  + the item's mention: the tokens of S's bridge item's name in its locker sentence, L..L+3 (locker-first: its
     earlier mention; locker-after: the same sentence after the asked pick, so 'wherever it appears')
  4  + the question's tokens, L..L+3: Zach's 'question' positions (ablate_v2.question_start: the question sentence and
     every token after it, the template's tail and the read's appended token included)
  5  every token of the read prompt, L..L+3 (the same 25 atoms at every token)
  6  every token, Zach's band (9B L12-16, Muse L23-29), Zach's definition by his code path: per token the projection on
     the span of the 10 J++ directions with the highest lens logits there, never a protected atom (the clean read's
     top-10 tokens; ablate.removal_edit("top", LensDictionary, RowSettings(protected=...)), as ablate_v2's paper10 with
     --positions all); random beside: per token a random subspace part of the share his removal takes from the state
     as it arrives (seed 888 + l)
The 27B runs the bridge-word rungs (1)-(2) only.

Rules (stage verdict; point estimates decide, EPS 1e-9 at the bars; cluster-bootstrap CIs over the bridge items, 10,000,
seed 0, beside): cost(rung) = kept(random) - kept(removal), the share of S's answers lost beyond random (raw cost
kept(none) - kept(removal) reported beside).
  second copy      "the second copy is the earlier mention": in locker-first scenes the recall's cost(3) - cost(2) >=
                   0.30 with its paired CI excluding 0, and in locker-after scenes the recall's cost(2) >= 0.30
  only everything  "needed only when everything goes": over all scenes the recall's cost at rungs 1-4 each <= 0.20 and
                   cost(5) or cost(6) >= 0.50
  lookup           "the lookup never needs it": over all scenes the lookup's cost <= 0.10 at every rung
Per order group the same numbers, descriptive. The 27B: numbers at rungs 1-2, no rule (bridge-word rungs only).

SEALED: the run writes per-item outputs only; verdict refuses until predictions/2026-10-28_dan.md holds Dan's Q49.2
answer at the committed HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x49_ladder.py plan                           # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x49_ladder.py run --name qwen35_9b_x49_2      # GPU (sealed)
uv run python scripts/x49_ladder.py verdict                                              # CPU, after Dan's Q49.2
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
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x47_zero as Z

EXP = "x49_ladder"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch49.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q49.2"
RENDERING = "chat"
SPAN = Z.SPAN  # L..L+3
K = X.K_MAIN  # the change's 25 OMP atoms
K_TOP = 10  # Zach's top-10
SOURCES = B.FRESH_RUN  # target -> its 45m run (the clean design)
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
RUNS = {"qwen3.5-9b": "qwen35_9b_x49_2", "qwen3.6-27b": "x49_2_27b", "muse-glimmer-30b": "muse30_x49_2_r2"}  # the first Muse run OOMed (28 Oct)
BAND = {"qwen3.5-9b": tuple(range(12, 17)), "muse-glimmer-30b": tuple(range(23, 30))}  # Zach's band; the 27B: none
RUNGS = (1, 2, 3, 4, 5, 6)
BRIDGE_RUNGS = (1, 2)  # the 27B's
RUNG_TEXT = {
    1: "the bridge word, at L",
    2: "the bridge word, at L..L+3",
    3: "+ the item's mention in its locker sentence, L..L+3",
    4: "+ the question's tokens, L..L+3",
    5: "every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token",
    6: "every token, Zach's band: his top-10 lens directions per token (his code path)",
}
KINDS = ("zero", "rand")
ORDERS = ("locker-first", "locker-after")
GROUPS = (*ORDERS, "all")
ORDER_OF = {"before": "locker-first", "after": "locker-after"}  # x0_strata's 'alt locker vs asked pick'
SECOND_COPY, QUIET, NEEDED, LOOKUP_NEVER = 0.30, 0.20, 0.50, 0.10
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULES = {
    "second_copy": "the second copy is the earlier mention: rung (3) costs the recall >= 0.3 more than rung (2) in "
                   "locker-first scenes (paired CI excluding 0) and rung (2) already costs >= 0.3 in locker-after scenes",
    "only_everything": "needed only when everything goes: rungs (1)-(4) each <= 0.2 and rung (5) or (6) >= 0.5",
    "lookup": "the lookup never needs it: <= 0.1 beyond random at every rung",
}  # fmt: skip
COST = "cost = kept(random) - kept(removal): S's answers lost beyond the random subspace of the same share, per rung"
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
TWO_DEFS = ("Rungs 5 and 6 are two definitions, not one: rung 5 removes, at every token, the span of the bridge's "
            "change's 25 OMP atoms (ours, L..L+3); rung 6 removes, at every token, that token's own top-10 lens "
            "directions (Zach's, over his band)")  # fmt: skip


def arms_of(rungs: tuple[int, ...]) -> tuple[str, ...]:
    """'none', then per rung its removal and its random beside: zero1, rand1, zero2, ..."""
    return ("none", *(f"{k}{r}" for r in rungs for k in KINDS))


def rung_of(arm: str) -> tuple[str, int | None]:
    return ("none", None) if arm == "none" else (arm[:4], int(arm[4:]))


# ---- positions and items (tokenizer only) --------------------------------------------------------------------------


class Dropped(ValueError):
    """An item the rungs cannot use (counted in the plan)."""


def rung_positions(n_tokens: int, pos: int, mention: list[int], question: list[int]) -> dict[int, list[int]]:
    """Each rung's token positions in the read prompt (n_tokens long, the appended space token included): nested,
    1 = 2 = the bridge word; 3 adds the item's mention; 4 the question's tokens; 5 = 6 = every token."""
    r3 = sorted({pos, *mention})
    r4 = sorted({*r3, *question})
    every = list(range(n_tokens))
    assert set(r4) <= set(every), "a rung's position is outside the prompt"
    return {1: [pos], 2: [pos], 3: r3, 4: r4, 5: every, 6: every}


def mention_span(text: str, context: str, item: str) -> list[int]:
    """The character span [start, end) of the item's name inside its (single) locker sentence in the rendered prompt."""
    from scripts import x45p

    lockers = x45p.locker_items(context)
    spans = B.locker_spans(text, context)
    mine = [k for k, (_, it) in enumerate(lockers) if it == item]
    if len(mine) != 1:
        raise Dropped(f"the item has {len(mine)} locker sentences")
    sent = lockers[mine[0]][0]
    i = spans[mine[0]][0] + B.LOCKER_RE.match(sent).span(1)[0]  # type: ignore[union-attr]
    return [i, i + len(item)]


def question_positions(tok, read_ids: list[int]) -> list[int]:
    """Zach's 'question' positions of the read prompt (ablate_v2.question_start on: the question sentence, the
    template's tail, the appended read token)."""
    from scripts.ablate_v2 import question_start

    return list(range(question_start(tok, read_ids), len(read_ids)))


def reader_record(tok, c: dict, src_item: dict, w: str) -> dict:
    """One reader's S prompt as read: its ids, the mention's and the question's positions, and the prompt with each
    rung's tokens marked (⟦bridge:…⟧, ⟦mention:…⟧, ⟦question:…⟧; rungs 5-6 take every token)."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import x45p

    rd = c["readers"][w]
    text = X.render(tok, src_item, RENDERING, c["cf_context"])
    enc = raw_encoding(tok, text, offsets=True)
    if enc["input_ids"] != rd["ids"]["alt"]:
        raise Dropped("the rendered S prompt's ids differ from the case's")
    suffix = tok.decode(c["space"])
    offsets = [tuple(o) for o in enc["offset_mapping"]]
    offsets += [(len(text) + sum(len(tok.decode([t])) for t in c["space"][:j]),
                 len(text) + sum(len(tok.decode([t])) for t in c["space"][: j + 1])) for j in range(len(c["space"]))]  # fmt: skip
    read_ids = rd["ids"]["alt"] + c["space"]
    mention = x45p.token_positions(offsets, mention_span(text, c["cf_context"], c["cf_bridge"]))
    if not x45p.exact(tok, read_ids, mention, c["cf_bridge"]):
        raise Dropped("the mention's tokens are not exactly the item's name")
    if c["pos"] in mention:
        raise Dropped("the mention overlaps the bridge word")
    question = question_positions(tok, read_ids)
    if min(question) <= max(c["pos"], *mention):
        raise Dropped("the question does not come after the bridge word and the mention")
    marks = [(a, b, role) for role, ps in (("bridge", [c["pos"]]), ("mention", mention), ("question", question))
             for a, b in B.merged_spans(offsets, ps)]  # fmt: skip
    return {**{k: rd[k] for k in ("id", "question", "answer", "cf_answer", "tok_A", "tok_b", "ids")},
            "mention": mention, "question_pos": question, "n_read": len(read_ids),
            "marked": x45p.marked(text + suffix, marks)}  # fmt: skip


def gate_of(src: Path) -> dict:
    g = json.loads((src / "gate.json").read_text())["gate"].get(RENDERING, {})
    assert g.get("pass"), f"{src.name}: its gate fixed in advance did not pass (chat)"
    return g


def select(tok, run: str, layer: int) -> tuple[list[dict], dict]:
    """The clean design's items in the 45m run's scene order, their order group and rung positions, and the counts."""
    from scripts import tasks_v2 as T
    from scripts import x0_strata as ST
    from scripts import x45m, x45p
    from scripts import x47_cumulative as C

    src = X.RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    assert m.get("alt") == "fresh", f"{run}: alt {m.get('alt')!r}, not 45m's fresh alt"
    assert m["predicted"] == layer, f"{run}: layer {m['predicted']}, not {layer}"
    assert m["model"]["target"] == pins.TARGET, f"{run} is a {m['model']['target']} run, not {pins.TARGET}'s"
    items_file = pins.DATA_DIR / "tasks_v2" / m["set"] / "items.jsonl"
    rel = str(items_file.relative_to(pins.REPO_ROOT))
    assert X.sha256_of(items_file) == m["inputs"][rel], f"{rel} changed since {run}"
    gate = gate_of(src)
    scenes, _ = C.stored_whole(src, layer)
    assert scenes, f"{run}: no chat outcomes at layer {layer}"
    old = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == RENDERING}
    rebuilt = {c["scene"]: c for c in x45p.rebuild(tok, m["set"])}
    by_id = {it["id"]: it for it in T.load(m["set"])}
    out, dropped = [], collections.Counter()
    for scene in scenes:
        c = rebuilt[scene]
        assert c["pos"] == old[scene]["pos"], f"{scene}: the bridge position moved since {run}"
        assert c["fresh"] == old[scene]["fresh"], f"{scene}: the inserted item changed since {run}"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == old[scene]["readers"][w]["ids"], f"{scene}: {w}'s ids changed"
        where = ST.features(c)["alt locker vs asked pick"]
        try:
            if where not in ORDER_OF:
                raise Dropped(f"the new item's locker sentence: {where}")
            for w in X.READERS:
                ids = c["readers"][w]["ids"]
                if C.changed_positions(ids["org"], ids["alt"]) != [c["pos"]]:
                    raise Dropped("O and S differ beyond the bridge word")
            readers = {w: reader_record(tok, c, by_id[c["readers"][w]["id"]], w) for w in X.READERS}
        except (Dropped, C.Misaligned) as e:
            dropped[str(e)] += 1
            continue
        mention = readers[X.LOOKUP]["mention"]
        assert readers[X.RECALL]["mention"] == mention, f"{scene}: the readers' mention positions differ"
        last = max(c["pos"], *mention)
        assert readers[X.RECALL]["ids"]["alt"][: last + 1] == readers[X.LOOKUP]["ids"]["alt"][: last + 1], (
            f"{scene}: the readers' prompts differ before the question"
        )
        order = ORDER_OF[where]
        assert (max(mention) < c["pos"]) == (order == "locker-first"), f"{scene}: the mention is on the wrong side"
        out.append({"scene": scene, "entity": c["bridge"], "cf_bridge": c["cf_bridge"], "domain": c["domain"],
                    "order": order, "group45m": x45m.group_of(c), "pos": c["pos"], "mention": mention,
                    "space": c["space"], "fresh": c["fresh"], "readers": readers})  # fmt: skip
    counts = {"source": run, "layer": layer, "gate": gate, "items_at_L": len(scenes), "dropped": dict(dropped),
              "items": len(out), "entities": len({it["entity"] for it in out}),
              "orders": dict(collections.Counter(it["order"] for it in out)),
              "group45m": dict(collections.Counter(f"{it['order']} / {it['group45m']}" for it in out)),
              "tokens_median": token_counts(out)}  # fmt: skip
    return out, counts


def token_counts(items: list[dict]) -> dict[str, dict[str, float]]:
    """Per reader, the median number of tokens each rung edits per layer."""
    out = {}
    for w in X.READERS:
        per = collections.defaultdict(list)
        for it in items:
            rd = it["readers"][w]
            for r, ps in rung_positions(rd["n_read"], it["pos"], it["mention"], rd["question_pos"]).items():
                per[r].append(len(ps))
        out[READER_NAME[w]] = {str(r): float(np.median(v)) for r, v in sorted(per.items())}
    return out


def example_indices(n: int, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def stage_plan(k: int = 5) -> Path:
    """Tokenizer only: the target's items and counts, and k random items (seed 0) with each rung's tokens marked."""
    from scripts import x45m

    tok = x45m.tokenizer()
    target = pins.TARGET
    layer = X.PREDICTED[target]
    items, counts = select(tok, SOURCES[target], layer)
    rungs = RUNGS if target in BAND else BRIDGE_RUNGS
    counts.update({"target": target, "layers": list(range(layer, layer + SPAN)), "band": list(BAND.get(target, ())),
                   "rungs": {str(r): RUNG_TEXT[r] for r in rungs}, "arms": list(arms_of(rungs)),
                   "reads": len(items) * len(X.READERS) * len(arms_of(rungs))})  # fmt: skip
    folder = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{pins.RUN_PREFIX.rstrip('_') or '27b'}"
    folder.mkdir(parents=True)
    lines = [f"# 49.2 plan on {target} (L{layer}; rungs {', '.join(map(str, rungs))}): {min(k, len(items))} of the clean "
             f"design's {len(items)} items (seed {X.EXAMPLES_SEED}), S's prompt as each reader reads it (the read's "
             "appended space token included).", "",
             "⟦bridge:…⟧ rungs 1-6 (the bridge word); ⟦mention:…⟧ rung 3 on (the item's name in its locker sentence); "
             "⟦question:…⟧ rung 4 on (Zach's 'question' positions); every token, marked or not, rungs 5-6. Counts in "
             "plan.json.", ""]  # fmt: skip
    for i in example_indices(len(items), k):
        it = items[i]
        lines += [f"## {it['scene']} ({it['domain']}, {it['order']}): bridge {it['entity']} -> {it['cf_bridge']}, "
                  f"token {it['pos']}, mention {it['mention']}", ""]  # fmt: skip
        for w, rd in it["readers"].items():
            ps = rung_positions(rd["n_read"], it["pos"], it["mention"], rd["question_pos"])
            lines += [f"**{READER_NAME[w]}** ({rd['id']}), S's answer {rd['cf_answer']}; tokens per rung: "
                      + ", ".join(f"({r}) {len(ps[r])}" for r in rungs), "", "```", rd["marked"], "```", ""]  # fmt: skip
    (folder / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    (folder / "prompts.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("wrote", folder)
    return folder


# ---- the edits (CPU-testable) --------------------------------------------------------------------------------------


class AtomsOut(Z.ProjectOut):
    """47.5's ProjectOut at every given position inside the sequence (a greedy prompt without the read's appended
    token is one shorter): h <- h - (h Q) Q^T."""

    def __call__(self, h):
        inside = [p for p in self.positions if p < h.shape[0]]
        return Z.ProjectOut(self.basis, inside)(h) if inside else h


class RandomOut:
    """The random beside a rung: at each position p, the state minus its projection on the first ks[j] columns of
    `basis` ([d, d], orthonormal columns; X0's random basis), ks[j] per token (R.random_k on S's clean state)."""

    def __init__(self, basis, positions: list[int], ks: list[int]):
        assert len(positions) == len(ks), "one k per position"
        self.basis, self.positions, self.ks = basis, positions, ks

    def __call__(self, h):
        import torch

        sel = [j for j, p in enumerate(self.positions) if p < h.shape[0]]
        if not sel:
            return h
        pos = [self.positions[j] for j in sel]
        b = self.basis.to(h.device, h.dtype)
        k = torch.tensor([self.ks[j] for j in sel], device=h.device)
        out = h.clone()
        rows = h[pos]
        coef = rows @ b
        coef = coef * (torch.arange(b.shape[1], device=h.device)[None, :] < k[:, None])
        out[pos] = rows - coef @ b.T
        return out


class ZachTop:
    """Rung 6, his code path: ablate.removal_edit('top', dic, [RowSettings(protected=...)], k=10) on the one sequence
    (every position, no sink skipped: ablate_v2's paper10 with --positions all). log: per call, the mean share of
    ||h||^2 removed over the positions."""

    def __init__(self, dic, protected, k: int = K_TOP):
        from bridge_jspace.ablate import RowSettings, removal_edit

        self.edit = removal_edit("top", dic, [RowSettings(protected=protected)], k=k)
        self.log: list[float] = []

    def removal(self, h):
        x = h.float()
        return x - self.edit(x[None])[0]

    def shares(self, h, r):
        return (r.norm(dim=-1) ** 2 / (h.float().norm(dim=-1) ** 2).clamp_min(1e-30)).float()

    def __call__(self, h):
        r = self.removal(h)
        self.log.append(float(self.shares(h, r).mean()))
        return h.float() - r


class ZachRandom(ZachTop):
    """The random beside rung 6: per token a random subspace part (statement_positions.random_subspace_part, X0's
    random basis) of the share of ||h||^2 his removal takes there, on the state as it arrives."""

    def __init__(self, dic, protected, basis, k: int = K_TOP):
        super().__init__(dic, protected, k)
        self.basis = basis

    def __call__(self, h):
        from scripts import statement_positions as SP

        x = h.float()
        share = self.shares(x, self.removal(x))
        part = SP.random_subspace_part(x, share, self.basis.to(x.device, x.dtype))
        self.log.append(float((part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)).mean()))
        return x - part


def edit_sets(rungs: tuple[int, ...], layers: tuple[int, ...], positions: dict[int, list[int]], q: dict, bases: dict,
              ks: dict, band: tuple[int, ...] = (), zdic: dict | None = None, protected=None) -> dict[str, dict]:  # fmt: skip
    """Each arm's edit set ({layer: edit}) for one item and reader, in arms_of(rungs) order. q[l]: the item's atom
    basis at layer l; bases[l]: the layer's random basis; ks[l]: [n_tokens] k per token of S's clean state at l;
    positions: rung_positions; zdic[l]: Zach's dictionary at each band layer, protected: his protected rows."""
    out: dict[str, dict] = {"none": {}}
    for r in rungs:
        if r == 6:
            assert band, "rung 6 needs Zach's band"
            assert zdic is not None, "rung 6 needs Zach's dictionaries"
            out["zero6"] = {la: ZachTop(zdic[la], protected) for la in band}
            out["rand6"] = {la: ZachRandom(zdic[la], protected, bases[la]) for la in band}
            continue
        ps = positions[r]
        at = layers[:1] if r == 1 else layers
        out[f"zero{r}"] = {la: AtomsOut(q[la], ps) for la in at}
        out[f"rand{r}"] = {la: RandomOut(bases[la], ps, [int(ks[la][p]) for p in ps]) for la in at}
    assert tuple(out) == arms_of(rungs)
    return out


def token_shares(h, q) -> Any:
    """[n] each row's share of ||h||^2 in the span of q's orthonormal columns (h [n, d], q [d, r])."""
    hd, qd = h.double(), q.double().to(h.device)
    return ((hd @ qd).norm(dim=-1) ** 2 / (hd.norm(dim=-1) ** 2).clamp_min(1e-30)).float()


# ---- GPU ------------------------------------------------------------------------------------------------------------


def band_dictionaries(model, lens, band: tuple[int, ...], letters) -> dict:
    """Zach's dictionaries over the band, built as ablate_v2 builds them: one W_g = W_U[letters] * the final norm's
    gain shared by every layer, LensDictionary(W_g, J_l) per layer (x47_twodefs.zach_dictionary builds W_g per call;
    one copy here, as a band of 7 copies would not fit beside Muse)."""
    from bridge_jspace.ablate import LensDictionary

    if not band:
        return {}
    import torch

    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    torch.cuda.empty_cache()
    # chunk 4096 for the row norms: the default 32768 x d fp32 block (832 MiB on Muse, d = 6656) did not fit beside
    # Muse's weights, W_g and the cached J_l / bases (x49_2_muse, 28 Oct: OOM); the norms are per row, so the result is
    # the same at any chunk.
    return {la: LensDictionary(wg, lens.J(la), chunk=4096) for la in band}


def run_items(model, lens, items: list[dict], layers: tuple[int, ...], band: tuple[int, ...], ws, digits,
              zach_dictionaries=None) -> tuple[list, list, list]:  # fmt: skip
    """The rungs on each item's S prompt, both readers: (outcome rows, per item and reader the shares removed, greedy
    texts of the example items). band = () runs the bridge-word rungs only (the 27B)."""
    import torch

    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R
    from scripts import x47_twodefs as TD

    zach_dictionaries = zach_dictionaries or band_dictionaries
    rungs = RUNGS if band else BRIDGE_RUNGS
    arms = arms_of(rungs)
    dev = model.device
    letters = model.letter_token_ids()
    h: dict[str, dict[int, list]] = {"org": {la: [] for la in layers}, "alt": {la: [] for la in layers}}
    for c in progress(items, "49.2: Δ at the bridge word (item)"):
        ids = c["readers"][X.LOOKUP]["ids"]
        for v in ("org", "alt"):
            rec = model.run(torch.tensor([ids[v]], device=dev), record=layers)[1]
            for la in layers:
                h[v][la].append(rec[la][c["pos"]].float())
    bases = {la: SP.random_basis(int(h["alt"][layers[0]][0].shape[0]),
                                 torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
             for la in sorted({*layers, *band})}  # fmt: skip
    q: dict[int, list] = {}
    bridge = [[] for _ in items]
    for la in layers:
        jdic = lens.vectors(la, letters)
        hs, ho = torch.stack(h["alt"][la]).to(dev), torch.stack(h["org"][la]).to(dev)
        q[la], _, per = Z.layer_parts(jdic, hs, ho, bases[la])
        q[la] = [b.cpu() for b in q[la]]
        del jdic
        for i, r in enumerate(per):
            bridge[i].append({"layer": la, **r})
    zdic = zach_dictionaries(model, lens, band, letters)
    row_of = torch.full((len(model.decoded),), -1, dtype=torch.long, device=dev)
    row_of[letters.to(dev)] = torch.arange(letters.numel(), device=dev)
    rows, norms, greedy = [], [], []
    examples = set(example_indices(len(items)))
    with torch.no_grad():
        for i, c in enumerate(progress(items, f"49.2: rungs {rungs[0]}-{rungs[-1]} (item)")):
            for w, rd in c["readers"].items():
                read_ids = rd["ids"]["alt"] + c["space"]
                clean, st = model.run(torch.tensor([read_ids], device=dev), record=layers)
                prot = TD.protected_rows(clean, row_of)
                positions = rung_positions(len(read_ids), c["pos"], c["mention"], rd["question_pos"])
                qi = {la: q[la][i].to(dev) for la in layers}
                share = {la: token_shares(st[la], qi[la]) for la in layers}
                ks = {la: R.random_k(st[la].float(), share[la], bases[la]).tolist() for la in layers}
                edits = edit_sets(rungs, layers, positions, qi, bases, ks, band, zdic, prot)
                logits, _ = X.read_logits(model, rd["ids"]["alt"], list(edits.values()), RENDERING, c["space"], ws)
                for arm, lg in zip(arms, logits, strict=True):
                    kind, rung = rung_of(arm)
                    r = X.read_row(lg, rd, digits)
                    rows.append({"scene": c["scene"], "entity": c["entity"], "domain": c["domain"], "order": c["order"],
                                 "reader": w, "arm": arm, "rung": rung, "kind": kind, "kept": r["switched"],
                                 "to_org": int(r["top"] == rd["tok_A"]), "cand_kept": r["cand_switched"],
                                 **{k: r[k] for k in ("top", "role", "p_org", "p_alt", "ld")}})  # fmt: skip
                sets = {"bridge": [c["pos"]], "mention": c["mention"], "question": rd["question_pos"],
                        "every": positions[5]}  # fmt: skip
                norms.append({"scene": c["scene"], "reader": w, "bridge": bridge[i] if w == X.LOOKUP else None,
                              "atoms_share": {str(la): {s: round(float(share[la][ps].mean()), 6) for s, ps in sets.items()}
                                              for la in layers},
                              # each rung-6 edit's first call is the read's (the greedy examples come after)
                              "zach_share": {f"{kd}6": {str(la): round(edits[f"{kd}6"][la].log[0], 6) for la in band}
                                             for kd in KINDS} if band else {},
                              "protected": prot.tolist()})  # fmt: skip
                if i in examples:
                    texts = model.generate_batch(torch.tensor([rd["ids"]["alt"]], device=dev), X.GEN_TOKENS,
                                                 list(edits.values()))  # fmt: skip
                    greedy += [{"scene": c["scene"], "reader": w, "arm": a, "greedy": t}
                               for a, t in zip(arms, texts, strict=True)]  # fmt: skip
    return rows, norms, greedy


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state
    from scripts import x6_routes as R

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "49.2 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in SOURCES, f"49.2 runs on {sorted(SOURCES)}, not {target}"
    layer, band = X.PREDICTED[target], BAND.get(target, ())
    layers = tuple(range(layer, layer + SPAN))
    assert max(*layers, *band) <= pins.N_LAYERS - 2, f"L..L+3 {layers} / band {band}: past the last block read on"
    rungs = RUNGS if band else BRIDGE_RUNGS
    run45 = SOURCES[target]
    src = X.RESULTS / run45
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "49.2",
         "spec": f"{SPEC} (49.2 and amendment 2's 49.2 item)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (pins.REPO_ROOT / SPEC, *(src / f for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl", "gate.json")))},
         "source": run45, "layer": layer, "layers": list(layers), "band": list(band), "k": K, "k_top": K_TOP,
         "rungs": {str(r): RUNG_TEXT[r] for r in rungs}, "arms": list(arms_of(rungs)),
         "omp": "signed (x0_parts.omp_atoms, X0's k = 25 picks), per layer of L..L+3 on Δ_l at the bridge word",
         "edit": "rungs 1-5: h <- h - (h Q_l) Q_l^T at the rung's tokens (Q_l: the bridge's Δ_l's 25 atoms), on the "
                 "state as it arrives; rung 6: ablate.removal_edit('top', LensDictionary(W_U[letters] * gain, J_l), "
                 "[RowSettings(protected=the clean read's top-10 rows)], k=10) at every token of each band layer",
         "random_part": f"rungs 1-5: per token the first k columns of X0's random basis (seed {X.SUBSPACE_SEED} + layer), "
                        "k so that they hold the atoms' share of that token's ||h_S||^2 on S's clean state (the reader's "
                        "read prompt) at that layer; rung 6: per token random_subspace_part at the share his removal "
                        "takes from the state as it arrives",
         "positions": {"mention": "the tokens of S's bridge item's name in its locker sentence (character offsets)",
                       "question": "ablate_v2.question_start onward: the question sentence, the template's tail and the "
                                   "read's appended token", "every": "every token of the read prompt, the appended one included"},
         "orders": "x0_strata 'alt locker vs asked pick': before = locker-first, after = locker-after; x45m's group beside",
         "items_rule": "the 45m run's scenes at L (chat), the items its unedited run made eligible (its gate passed); "
                       "O and S differ only at the bridge word; the mention's tokens exactly the item's name; else "
                       "dropped and counted (plan.json)",
         "read": "X0's chat read of S: the prompt with a digit's space token appended; kept = the top token is S's "
                 "answer's first token", "tf32": "off (fp32 matmuls; ablate_v2 turns TF32 on for speed)",
         "rules": RULES, "cost": COST, "two_definitions": TWO_DEFS,
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "examples": X.EXAMPLES_SEED}, "n_boot": X.N_BOOT,
         "order": {"items": "the 45m run's scene order", "reads": "per item and reader: S's read prompt under the arms "
                   "in arms order, batched (BJ_SUITE_BATCH)"},
         "sealed": f"no verdict in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    torch.backends.cuda.matmul.allow_tf32 = False
    lens = JLens(model, "jpp")  # check_frozen: the file's sha256 is pins.FROZEN_LENS_SHA256
    missing = [la for la in sorted({*layers, *band}) if la not in lens.source_layers]
    assert not missing, f"the J++ lens has no map at layers {missing} (L..L+3 = {layers}, band {band})"
    items, counts = select(model.tokenizer, run45, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(model.tokenizer), device=model.device)
    rows, norms, greedy = run_items(model, lens, items, layers, band, ws, digits)
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "norms.jsonl", norms)
    X.write_jsonl(out / "examples_greedy.jsonl", greedy)
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- verdict (CPU, sealed) ------------------------------------------------------------------------------------------


def dan_answer(rev: str = "HEAD") -> str:
    """Dan's committed answer to Q49.2 (the 'Dan:' line of its block in the predictions file at `rev`), '' if none."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout  # fmt: skip
    if f"**{QUESTION}**" not in text:
        return ""
    block = text.split(f"**{QUESTION}**", 1)[1].split("\n**Q", 1)[0]
    found = re.search(r"^Dan(?: \([^)]*\))?:(.*(?:\n(?:Dan(?: \([^)]*\))?:|- ).*)*)", block, re.M)
    return found.group(1).strip() if found else ""


def unsealed() -> str:
    answer = dan_answer()
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def numbers(rows: list[dict], reader: str, rungs: tuple[int, ...], n_boot: int = X.N_BOOT,
            seed: int = X.BOOT_SEED) -> dict:  # fmt: skip
    """One reader's numbers over the given rows: kept per arm, cost per rung (kept(rand) - kept(zero), paired) and raw
    cost (kept(none) - kept(zero)), and cost(3) - cost(2) where rung 3 ran; cluster-bootstrap CIs over the bridge
    items."""
    arms = arms_of(rungs)
    by: dict[tuple[str, str], int] = {}
    entity: dict[str, str] = {}
    for r in rows:
        if r["reader"] == reader:
            entity.setdefault(r["scene"], r["entity"])
            by[(r["scene"], r["arm"])] = int(r["kept"])
    scenes = list(entity)
    if not scenes:
        return {"n": 0}
    missing = [(s, a) for s in scenes for a in arms if (s, a) not in by]
    assert not missing, f"{reader}: {len(missing)} item-arm reads missing, e.g. {missing[:3]}"
    kept = {a: [by[(s, a)] for s in scenes] for a in arms}
    boot = X.resampled_rates(kept, [entity[s] for s in scenes], n_boot, seed)
    pt = {a: float(np.mean(v)) for a, v in kept.items()}

    def iv(p: float, b) -> list[float]:
        return [p, *X.interval(b)]

    cost = {r: iv(pt[f"rand{r}"] - pt[f"zero{r}"], boot[f"rand{r}"] - boot[f"zero{r}"]) for r in rungs}
    out = {"n": len(scenes), "entities": len(set(entity.values())), "kept": {a: iv(pt[a], boot[a]) for a in arms},
           "cost": {str(r): v for r, v in cost.items()},
           "raw_cost": {str(r): iv(pt["none"] - pt[f"zero{r}"], boot["none"] - boot[f"zero{r}"]) for r in rungs}}  # fmt: skip
    if 3 in rungs:
        d = (boot["rand3"] - boot["zero3"]) - (boot["rand2"] - boot["zero2"])
        out["cost3_minus_cost2"] = iv(cost[3][0] - cost[2][0], d)
    return out


def rules(cells: dict[str, dict]) -> dict[str, Any]:
    """The three rules on one model's cells ({reader: {group: numbers}}), rungs 1-6 (point estimates; EPS at the
    bars; the second copy also needs the paired CI of cost(3) - cost(2) excluding 0)."""
    rc, lk = cells["recall"], cells["lookup"]
    first, after, every = rc["locker-first"], rc["locker-after"], rc["all"]
    d = first.get("cost3_minus_cost2") if first.get("n") else None
    c2_after = after["cost"]["2"][0] if after.get("n") else math.nan
    second = bool(d is not None and d[0] >= SECOND_COPY - EPS and d[1] > 0 and c2_after >= SECOND_COPY - EPS)
    c = {int(r): v[0] for r, v in every["cost"].items()}
    only = all(c[r] <= QUIET + EPS for r in (1, 2, 3, 4)) and max(c[5], c[6]) >= NEEDED - EPS
    never = all(v[0] <= LOOKUP_NEVER + EPS for v in lk["all"]["cost"].values())
    return {"second_copy": second, "only_everything": only, "lookup": never,
            "read": {"locker-first cost(3) - cost(2)": d, "locker-after cost(2)": c2_after,
                     "all: recall cost by rung": c, "all: lookup cost by rung": {int(r): v[0] for r, v in lk["all"]["cost"].items()}}}  # fmt: skip


def model_result(target: str, run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's run: pending (not here), or per reader and group its numbers, the rules (rungs 1-6 only), the
    median shares removed."""
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        return {"target": target, "run": run, "status": "pending", "why": "no manifest or outcomes here"}
    m = json.loads((src / "manifest.json").read_text())
    assert m["model"]["target"] == target, f"{run} is a {m['model']['target']} run, not {target}'s"
    rungs = tuple(int(r) for r in m["rungs"])
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cells = {READER_NAME[w]: {g: numbers([r for r in rows if g == "all" or r["order"] == g], w, rungs, n_boot)
                              for g in GROUPS} for w in X.READERS}  # fmt: skip
    out = {"target": target, "run": run, "status": "tested", "layer": m["layer"], "layers": m["layers"],
           "band": m["band"], "rungs": list(rungs), "cells": cells, "shares_median": shares_median(src, m)}  # fmt: skip
    out["rules"] = rules(cells) if rungs == RUNGS else None
    return out


def shares_median(src: Path, m: dict) -> dict:
    """Median over items and readers: the atoms' share of ||h_S||^2 at each token set per layer, and the share rung 6
    (and its random) removes per band layer."""
    norms = X.read_jsonl(src / "norms.jsonl")
    out: dict[str, Any] = {"atoms": {}, "zach": {}}
    for la in m["layers"]:
        out["atoms"][str(la)] = {s: float(np.median([n["atoms_share"][str(la)][s] for n in norms]))
                                 for s in ("bridge", "mention", "question", "every")}  # fmt: skip
    for kd in KINDS:
        if m["band"]:
            out["zach"][f"{kd}6"] = {str(la): float(np.median([n["zach_share"][f"{kd}6"][str(la)] for n in norms]))
                                     for la in m["band"]}  # fmt: skip
    return out


def fmt(v) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    lines = ["# 49.2: the removal ladder", "",
             f"Batch 49, test 49.2 ({SPEC} and amendment 2; {QUESTION}, Dan: {answer}). Clean design (45m), on S; "
             f"both readers, kept = S's answer read (X0's chat read). {COST}. Cluster bootstrap over the bridge items "
             f"({n_boot}, seed {X.BOOT_SEED}). {TWO_DEFS}. UNVERIFIED.", "",
             "Rules (fixed in advance; point estimates, over all scenes unless named): "
             + "; ".join(f"{k}: {t}" for k, t in RULES.items()) + ".", "",
             "| model | run | n | the second copy is the earlier mention | needed only when everything goes | the "
             "lookup never needs it |", "|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            lines.append(f"| {m['target']} | {m['run']} | {m['status']} ({m['why']}) | | | |")
            continue
        n = m["cells"]["recall"]["all"]["n"]
        if m["rules"] is None:
            lines.append(f"| {m['target']} | {m['run']} | {n} | bridge-word rungs only | | |")
            continue
        ru = m["rules"]
        lines.append(f"| {m['target']} | {m['run']} | {n} | **{'yes' if ru['second_copy'] else 'no'}** | "
                     f"**{'yes' if ru['only_everything'] else 'no'}** | **{'yes' if ru['lookup'] else 'no'}** |")  # fmt: skip
    lines += ["", "## Kept share and cost per rung", "",
              "| model | reader | group | n | none | " + " | ".join(f"rung {r}: removed / random / cost" for r in RUNGS)
              + " | cost(3) - cost(2) |", "|---|---|---|---|---|" + "---|" * (len(RUNGS) + 1)]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for w in ("recall", "lookup"):
            for g in GROUPS:
                c = m["cells"][w][g]
                if not c["n"]:
                    lines.append(f"| {m['target']} | {w} | {g} | 0 |" + " |" * (len(RUNGS) + 2))
                    continue
                cols = [f"{c['kept'][f'zero{r}'][0]:.2f} / {c['kept'][f'rand{r}'][0]:.2f} / {fmt(c['cost'][str(r)])}"
                        if str(r) in c["cost"] else "-" for r in RUNGS]  # fmt: skip
                lines.append(f"| {m['target']} | {w} | {g} | {c['n']} | {c['kept']['none'][0]:.2f} | " + " | ".join(cols)
                             + f" | {fmt(c.get('cost3_minus_cost2'))} |")  # fmt: skip
    lines += ["", "Raw cost (kept(none) - kept(removal)), beside:", "",
              "| model | reader | group | " + " | ".join(f"rung {r}" for r in RUNGS) + " |",
              "|---|---|---|" + "---|" * len(RUNGS)]  # fmt: skip
    for m in models:
        if m["status"] != "tested":
            continue
        for w in ("recall", "lookup"):
            for g in GROUPS:
                c = m["cells"][w][g]
                if c["n"]:
                    lines.append(f"| {m['target']} | {w} | {g} | "
                                 + " | ".join(fmt(c["raw_cost"].get(str(r))) for r in RUNGS) + " |")  # fmt: skip
    lines += ["", "Shares removed (median over items and readers): the bridge's 25 atoms' share of ||h_S||^2 per token "
              "set and layer; rung 6's removed share per band layer (his top-10; the random's achieved share).", ""]  # fmt: skip
    for m in models:
        if m["status"] == "tested":
            lines.append(f"- {m['target']}: atoms {json.dumps(m['shares_median']['atoms'])}; rung 6 "
                         f"{json.dumps(m['shares_median']['zach'])}")  # fmt: skip
    lines += ["", "Rungs: " + "; ".join(f"({r}) {t}" for r, t in RUNG_TEXT.items()) + "."]
    return lines


def example_lines(target: str, run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """The verify-pack view of one run: k random items (seed), each reader's S prompt as read with each rung's tokens
    marked, each arm's answer (the top token, kept or not) and greedy text."""
    src = RESULTS / run
    items = X.read_jsonl(src / "cases.jsonl")
    m = json.loads((src / "manifest.json").read_text())
    reads = {(r["scene"], r["reader"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples_greedy.jsonl")}
    lines = [f"## {target}: {run}, {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
    for i in example_indices(len(items), k, seed):
        c = items[i]
        lines += [f"### {c['scene']} ({c['domain']}, {c['order']}): bridge {c['entity']} (O) → {c['cf_bridge']} (S), "
                  f"token {c['pos']}", ""]  # fmt: skip
        for w, rd in c["readers"].items():
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "",
                      "```", rd["marked"], "```", "", "| arm | what | top token | kept S's | greedy |", "|---|---|---|---|---|"]  # fmt: skip
            for arm in m["arms"]:
                r = reads[(c["scene"], w, arm)]
                kind, rung = rung_of(arm)
                what = (
                    "S unedited"
                    if rung is None
                    else f"{'removed' if kind == 'zero' else 'random beside'}: {RUNG_TEXT[rung]}"
                )
                lines.append(
                    f"| {arm} | {what} | {r['top']} ({r['role']}) | {r['kept']} | {greedy.get((c['scene'], w, arm))!r} |"
                )
            lines.append("")
    return lines


def stage_verdict(runs: dict[str, str] | None = None, n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    runs = runs or RUNS
    models = [model_result(t, runs[t], n_boot) for t in MODELS]
    out = RESULTS / f"x49_2-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    (out / "x49_2.json").write_text(json.dumps({"dan": answer, "rules": RULES, "cost": COST, "two_definitions": TWO_DEFS,
                                                "rung_text": RUNG_TEXT, "models": models}, indent=1) + "\n")  # fmt: skip
    (out / "x49_2.md").write_text("\n".join(lines) + "\n")
    ex = ["# 49.2 verify pack: S's prompts as the model reads them (the read appends the digit's space token); "
          "⟦bridge:…⟧ rungs 1-6, ⟦mention:…⟧ rung 3 on, ⟦question:…⟧ rung 4 on, every token rungs 5-6. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] == "tested":
            ex += example_lines(m["target"], m["run"])
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name", help="run: the run name (results/x49_ladder/<name>/)")
    ap.add_argument("--why", default="batch 49, test 49.2 (jobs/c3/batch49.yaml; Q49.2): the removal ladder; sealed")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--runs", nargs=3, default=None, metavar=("9B", "27B", "MUSE"),
                    help=f"verdict: runs in place of the specs' {[RUNS[t] for t in MODELS]}")  # fmt: skip
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    else:
        stage_verdict(dict(zip(MODELS, a.runs, strict=True)) if a.runs else None, n_boot=a.n_boot)


if __name__ == "__main__":
    main()
