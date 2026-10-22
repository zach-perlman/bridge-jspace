"""pointer_swap (Dan's D3, 2026-10-20): what do the question tokens carry in transit when a recalled bridge feeds an
in-prompt lookup: the bridge's identity, a pointer to the binding statement's position, or the answer itself?

Items: scripts/pointer_v1.py (data/pointer_v1/<set>/), or any generator with the same item schema chosen by --data
(pointer_v2: offset-shift and reflexive scenes; pointer_v3: one statement more or fewer; pointer_v4: three topics with
many entities and three wordings; code_pointer_v1: Python code; alias_pointer_v1: statements in other languages; on
another target (BJ_TARGET), scenes whose prompts are not token-aligned under its tokenizer are dropped before sampling
and counted in summary counts.unaligned_scenes). Each base item has a token-aligned source "dissoc" whose residual,
patched into the base, predicts four distinct answers (none = the base answer; identity = the base's digit for the
source's entity; position = the base's digit at the source's queried slot; value = the source's answer, absent from the
base context; for RR value = identity by construction).

Edits (activation patching: the base's block output at the positions replaced by the source's), on the read prompt:
  groups   question (the question's tokens, cue included), final (every token after the question: instruction,
           template, 'Answer:'), last (the read's last two tokens, ':' and the appended space, where lookback work puts
           the pointer at mid-late depth before the value), both (question + final)
  layers   one at a time (the manifest's list, every 2nd or 4th layer), and windows (all layers of the window at once;
           default early 16-28, mid 32-40, transit 44-52 on the 27B, the same depth fractions elsewhere)
  sources  dissoc (the 4-way prediction); controls: same (q_s = q_b at the same slot with the same digit, the rest of the
           context reshuffled and redigited: every hypothesis predicts the base answer, so a change is damage), rand (a
           seeded random direction with the dissoc patch's per-position norm, added), other (a random item of another
           domain, same family and level: its residual at the positions the same distance from the prompt's end, added
           as a difference rescaled per position to the dissoc patch's norm); rand and other at every `control_stride`-th
           layer of the list
  checks   per item: the unedited base read; base patched into base at the middle layer (must be a no-op); the dissoc
           source patched at every position at layer 0 (must reproduce the source's own read: the hook's positive
           control)
Scoring (suite_split's answer read): one forward with the digit answer's space token appended; the top token's role:
none / identity / position / token / value (in that priority; token only where the data predicts it) / context
(another digit of the base context) / recall (a recalled digit of q_b, q_s or p; lookups only) / other_digit / other;
p of each predicted digit.

Decision rule (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window
x source dissoc), pooled over domains, Wilson 95% intervals over items:
  - interpretable iff the dissoc patch changes the answer (1 - share none: lower bound >= 0.20) and the same control
    changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"
  - verdict X in {identity, position, value} (RR: identity, position) iff X's lower bound exceeds the upper bounds of
    the other two and the chance bar: the rand control's upper bound for X at that layer (windows: the max over the
    window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)
  - otherwise "mixed". Primary: RL, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:
    position; H-word (or a lexical key): identity; H-value: value. DL is the reference (classic binding retrieval),
    RR the contrast (a pointer is useless there).
  - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->
    prompt RK / named -> prompt DK / RR).
Decision rule, pointer_v2 additions (fixed 2026-10-21, before any v2 run):
  - offset-shift levels (e<N>-off): the same rule with candidates {identity, position, token, value} (RR: identity,
    position, token). position = the order-slot pointer (H-order), token = the token-position pointer (H-token).
  - reflexive vs plain (e<N>-ref vs e<N>-pln, the same scenes): per family x group x layer or window, the paired
    difference of the 'value' share (ref minus pln; items paired by scene; paired bootstrap 95% CI, seed 0).
    H-reflexive (a pointer to the answer token, which needs the digit in the prompt): lower bound > +0.10. H-value
    (the digit carried as content): the CI inside [-0.10, +0.10]. Otherwise unclear. Interpreted only where the pln cell
    is interpretable by the rule above (changes >= 20% lower bound, same control <= 10% upper bound).
  - every cut the rule is applied to needs n >= 35 (the same control's bound); cuts below are reported, not judged.
Decision rule, pointer_v3 additions (fixed 2026-10-21, before any v3 run):
  - the alt prompt has one statement more (e5more) or one fewer (e5fewer) than the org prompt; the candidates are
    {identity, position (the slot counted from the start), end (counted from the end), token, value}; the per-digit
    chance bar from unpredicted context digits is 0 (all five org statements are predicted), the random push's stays.
  - primary cells: memory -> prompt, the last two tokens and the tokens after the question, layers 48 and 50 and the
    window 44-52, per alt type pooled over topics; a verdict counts as the answer only if it holds for both alt types
    (one more and one fewer), otherwise it is reported as type-dependent.
Decision rule, pointer_v4 additions (fixed 2026-10-21, before any v4 run):
  - intervals: every bound the rule reads (changed, the same control, the candidates, the random push, context) is the
    entity-cluster bootstrap 95% interval (the asked entity resampled with replacement within each topic, 2000
    resamples, seed 0; stats.cluster_bootstrap), widened to the item-level Wilson interval where that is wider (a
    percentile bootstrap has zero width at 0 or n events); item-level Wilson is reported next to it. Every cell reports
    n items / k asked entities / t wordings. The rule itself is unchanged.
Decision rule, pointer_v4x additions (fixed 2026-10-21, before any v4x run; pointer_v2's filler-moved and pointer_v3's
one-more / one-fewer layouts on pointer_v4's topics, wordings and entity-cluster intervals):
  - PRIMARY cells: memory -> prompt, the last two tokens, layers 48 and 50 (single layers, not the 44-52 window, where
    the digit has already arrived by 52), pooled over topics and per topic. On another target: the manifest's
    primary_layers (--primary-layers), placed by function (before the fetched digit arrives) before the run; "48 or 50"
    below then reads "any one of them".
  - e5-off: "order beats the same place in the text" at a layer iff the lower bound of the order slot (position) exceeds
    the upper bound of the same token position (token). H-order-v4 holds iff, at layer 48 or 50, this is true pooled
    and in at least 2 of the 3 topics (at the same layer).
  - e5more / e5fewer: "from the start beats from the end and the same place" at a layer iff the lower bound of the slot
    counted from the start (position) exceeds the upper bounds of the slot counted from the end (end) and of the same
    token position (token). H-start-v4 holds iff, at layer 48 or 50, this is true pooled and in at least 2 of the 3 topics
    for both alt types (one more and one fewer; at the same layer).
  - The rule's verdict (all candidates, controls) is reported for the same cells, and every other cell, the window and
    the after-question tokens are reported, not decisive. A per-topic cell needs n >= 35.
Decision rule, pointer_v6 additions (fixed 2026-10-21, before any v6 run; the same scenes under four layouts):
  - e5-abs: one prompt has an extra sentence (a statement's length) before the list: bridge alt's statement keeps its
    order index and its distance back from the question, and sits at the token position of the org's neighbour
    (token). e5-rel: one prompt has it between the list and the question: order index and token position stay, the
    distance back names the org's neighbour (back). These sources differ in length from the org prompt and are patched
    aligned from the end (the question and every token after it line up); no layer-0 all-position check for them.
    e5-still: the same extra sentence in the same place in both prompts. e5-long: e5-still with every statement about
    twice as long (a trailing clause, the same clauses in both prompts).
  - PRIMARY cells: memory -> prompt, the last two tokens, the primary layers (48 and 50 on the 27B; another target's
    --primary-layers), pooled over topics; a hypothesis holds if its test passes at any one primary layer with n >= 35
    in both levels compared. Differences: Newcombe 95% intervals on items.
  - H-rel (Dan): share(back | e5-rel) - share(token | e5-abs) has lower bound > 0. H-abs: the same difference has
    upper bound < 0. H-ordinal: in both e5-abs and e5-rel, the same slot's lower bound exceeds the moved statement's
    upper bound (token / back). H-long (Dan): share(position | e5-long) - share(position | e5-still) has upper bound
    < 0. Per-topic cells, named -> prompt, other layers and the full rule's verdicts are reported, not decisive.
Decision rule, pointer_v5 additions (fixed 2026-10-21, before any v5 run; the same scenes with digit and with
colour-word answers, 5 and 8 statements):
  - the rule above with the pointer_v4 additions (entity-cluster intervals) at the last two tokens, memory -> prompt,
    each primary layer (48 and 50 on the 27B; another target's --primary-layers). A level "keeps the slot" iff at one
    primary layer the verdict is "same statement slot" pooled and in >= 2 of 3 topics (cells with n >= 35).
  - H-word: e5-word keeps the slot. H-long: e8-digit keeps the slot. e5-digit (pointer_v4's layout again) and
    e8-word are reported with the same test. Word answers are read right after 'Answer:' (the word's first token with
    its leading space), digits after the appended space token, so "the last two tokens" are the read's last two.

Stages:  manifest --name N --why W [--data pointer_v1|pointer_v2|code_pointer_v1|alias_pointer_v1] --set S
                  [--levels ...] [--families ...] [--domains ...] [--family-roles P R C] [--n K] [--layers ...]
                  [--control-stride 2] [--groups ...] [--question-max-layer L] [--control-levels ...]
                  [--competence RUN | --no-eligibility]
         analyze --name N | figures --name N (CPU; a new analysis-<stamp>-figures/, replacing the run's previous one)
         run --name N          summarise --name N (re-aggregates into a new analysis-<stamp>/)
         examples --name N [--k 3] [--seed 0] (results/pointer_swap/N/examples.json)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "pointer_swap"
RESULTS = pins.RESULTS_DIR / EXP
GROUPS = ("question", "final", "last", "both")
SOURCES = ("dissoc", "same", "rand", "other")
ROLES = ("none", "identity", "position", "end", "token", "back", "value", "context", "recall", "other_digit", "other")
# every prediction a dataset may record, in priority order (end: pointer_v3's slot counted from the end of the list;
# back: pointer_v6's statement as far back from the question as bridge alt's in the alt prompt)
HYPS = ("none", "identity", "position", "end", "token", "back", "value")
POINTER_ROLES = ("end", "token", "back")  # predicted only by some levels
DATASETS = (
    "pointer_v1",
    "pointer_v2",
    "pointer_v3",
    "pointer_v4",
    "pointer_v4x",
    "pointer_v5",
    "pointer_v6",
    "code_pointer_v1",
    "alias_pointer_v1",
)
# Interval method per dataset (pointer_v4 additions in the docstring); Wilson for every other dataset.
CLUSTER_CI = {"kind": "entity_cluster", "cluster": "asked entity", "strata": "domain", "n_boot": 2000, "seed": 0,
              "bounds": "the wider of the cluster bootstrap and the item-level Wilson interval"}  # fmt: skip
CI_BY_DATA = {"pointer_v4": CLUSTER_CI, "pointer_v4x": CLUSTER_CI, "pointer_v5": CLUSTER_CI, "pointer_v6": CLUSTER_CI}
V4X_LAYERS = ("48", "50")  # pointer_v4x's primary layers on the 27B (the docstring's pointer_v4x additions)


def primary_layers(m: dict) -> tuple[str, ...]:
    """pointer_v4x's primary layers: the manifest's --primary-layers (another target's layers placed by function before
    its run), else the 27B's 48 and 50."""
    return tuple(str(la) for la in m.get("primary_layers") or V4X_LAYERS)


V4X_TESTS = {"e5-off": ("position", ("token",)), "e5more": ("position", ("end", "token")),
             "e5fewer": ("position", ("end", "token"))}  # level -> (winner, the outcomes it must beat)  # fmt: skip
# primary (lookup of a recalled bridge), reference (named lookup), contrast (recall) family per dataset
FAMILY_ROLES = {"code_pointer_v1": ("RK", "DK", "RR")}
DEFAULT_ROLES = ("RL", "DL", "RR")
WINDOW_FRACTIONS = {"early": (16 / 64, 28 / 64), "mid": (32 / 64, 40 / 64), "transit": (44 / 64, 52 / 64)}
SAMPLE_SEED, NULL_SEED, OTHER_SEED, EXAMPLE_SEED = 0, 0, 0, 0
BATCH = int(os.environ.get("BJ_BATCH", "64"))  # edited reads per batched call; smaller on a shared GPU (a smoke)
CHANGED_MIN, DAMAGE_MAX = 0.20, 0.10


def default_layers(step: int = 2) -> list[int]:
    return list(range(0, pins.N_LAYERS - 3, step))


def default_windows() -> dict[str, list[int]]:
    n = pins.N_LAYERS
    return {w: list(range(round(lo * n), round(hi * n) + 1)) for w, (lo, hi) in WINDOW_FRACTIONS.items()}


class SetRows:
    """Edit for one layer: the rows at `positions` replaced by `rows` [P, d] (activation patching)."""

    def __init__(self, rows: torch.Tensor, positions: list[int]):
        self.rows, self.positions = rows, positions

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = self.rows.to(h.dtype)
        return out


class AddRows:
    def __init__(self, delta: torch.Tensor, positions: list[int]):
        self.delta, self.positions = delta, positions

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = h[self.positions] + self.delta.to(h.dtype)
        return out


def null_rows(delta: torch.Tensor, generator: torch.Generator) -> torch.Tensor:
    r = torch.randn(delta.shape, device=delta.device, generator=generator)
    return torch.nn.functional.normalize(r, dim=-1) * delta.norm(dim=-1, keepdim=True)


# ---- items ----------------------------------------------------------------------------------------------------------


def prompt_text(tok, ctx: str, question: str) -> str:
    return S.render(tok, ctx, question)


def question_span(tok, text: str, question: str) -> tuple[list[int], list[int], list]:
    """(question token indices, indices of every token after the question, offsets) of a rendered prompt."""
    from bridge_jspace.tokens import raw_encoding

    offs = raw_encoding(tok, text, offsets=True)["offset_mapping"]
    q0 = text.rindex("\n" + question) + 1
    q1 = q0 + len(question)
    return (
        [i for i, (s, e) in enumerate(offs) if e > q0 and s < q1],
        [i for i, (s, _) in enumerate(offs) if s >= q1],
        offs,
    )


def answer_kind(item: dict) -> str:
    """'digit', or 'word' for any other answer kind (pointer_v5's 'colour')."""
    return "digit" if item.get("answer_kind", "digit") == "digit" else "word"


def prepare(item: dict, tok) -> dict[str, Any]:
    """Token ids (read form: the space token appended) of the base and the sources, and the position groups. Sources
    are token-aligned with the base, or, for items with align = "end" (pointer_v6's shifted contexts), aligned from
    the end: the question and every token after it have the same length, the context may differ, and base position i
    maps to source position i + shift[source]."""
    from bridge_jspace.tokens import raw_encoding

    # suite_v1's read: a digit answer after 'Answer:' plus the space token; a word answer (pointer_v5's colours) right
    # after 'Answer:', its first token carrying the leading space (S.answer_token)
    space = S.ids(tok, " ") if answer_kind(item) == "digit" else []
    texts = {"base": (item["context"], item["question"])}
    texts |= {s: (v["context"], v["question"]) for s, v in item["sources"].items()}
    rendered = {k: prompt_text(tok, c, q) for k, (c, q) in texts.items()}
    enc = raw_encoding(tok, rendered["base"], offsets=True)
    ids = {k: S.ids(tok, t) for k, t in rendered.items()}
    assert ids["base"] == list(enc["input_ids"]), f"{item['id']}: raw encoding differs"
    shift = {k: len(v) - len(ids["base"]) for k, v in ids.items()}
    if item.get("align") != "end":
        assert not any(shift.values()), f"{item['id']}: sources not token-aligned"
    question, final, offs = question_span(tok, rendered["base"], item["question"])
    for k in ids:
        assert [ids[k][i + shift[k]] for i in final] == [ids["base"][i] for i in final], (
            f"{item['id']}: template differs ({k})"
        )
        if shift[k]:  # the source's question sits at the same distance from the end
            s_question, _, _ = question_span(tok, rendered[k], texts[k][1])
            assert s_question == [i + shift[k] for i in question], (
                f"{item['id']}: question not aligned from the end ({k})"
            )
    n = len(ids["base"])
    return {
        "text": rendered["base"],
        "source_text": rendered["dissoc"],
        "offsets": offs,
        "shift": shift,
        "read_ids": {k: v + space for k, v in ids.items()},
        "groups": {
            "question": question,
            "final": final,
            "last": [n + len(space) - 2, n + len(space) - 1],  # the read's last two tokens
            "both": question + final,
            "all": list(range(n + len(space))),
        },
    }


def role_map(item: dict, preds: dict[str, str], lookup: bool) -> dict[str, str]:
    """digit -> role, by the docstring's priority."""
    out: dict[str, str] = {}
    for h in HYPS:
        if preds.get(h, "-") != "-":
            out.setdefault(preds[h], h)
    for d in item["digits"]:
        out.setdefault(str(d), "context")
    rec = item.get("recalled", {})
    if lookup and rec:
        ents = [item["query"], item["sources"]["dissoc"].get("query")]
        for key in ("position", "token", "back"):
            j = item["slots"].get(key)
            if isinstance(j, int) and j < len(item["entities"]):
                ents.append(item["entities"][j])
        for e in ents:
            if e in rec:
                out.setdefault(str(rec[e]), "recall")
    return out


def wording_of(item: dict) -> dict[str, str]:
    """pointer_v4's wording ('<statement template>/<question template>') and held-out cut, for the outcome rows."""
    t = item.get("templates")
    return {"template": f"{t['statement']}/{t['question']}", "cut": item.get("cut", "-")} if t else {}


def slot_class(item: dict) -> str:
    """first / middle / last statement for the base query (Mixing Mechanisms: positional binding dominates only at the
    ends; lexical and reflexive routes take over in the middle)."""
    a = item["slots"]["query"]
    return "first" if a == 0 else "last" if a == item["n_entities"] - 1 else "middle"


def other_predictions(item: dict, other: dict) -> dict[str, str]:
    """For the 'other' control: none; position = the base digit at the other item's queried slot (if not the base's);
    value = the other's answer if absent from the base context. No identity (another domain)."""
    k = other["slots"]["query"]
    p = {"none": item["answer"], "identity": "-", "position": "-", "value": "-"}
    if k != item["slots"]["query"] and k < len(item["digits"]) and item["family"] != "RR":
        p["position"] = str(item["digits"][k])
    if item["family"] != "RR" and other["answer"] not in {str(d) for d in item["digits"]}:
        p["value"] = other["answer"]
    return p


def gen(m: dict | str):
    """The generator module of a run's items (same item schema): pointer_v1 (the default; older manifests have no
    'data'), pointer_v2, code_pointer_v1 or alias_pointer_v1. Each has DATA, RESULTS, SETS, FAMILIES, DOMAINS and
    set_files(set) -> {'<domain>_<family>_<level>': file}."""
    import importlib

    return importlib.import_module(f"scripts.{m if isinstance(m, str) else m.get('data', 'pointer_v1')}")


def family_roles(m: dict) -> tuple[str, str, str]:
    """(primary, reference, contrast) families: memory -> prompt, named -> prompt, memory -> memory."""
    return tuple(m.get("family_roles") or FAMILY_ROLES.get(m.get("data", "pointer_v1"), DEFAULT_ROLES))  # type: ignore[return-value]


def base_level(level: str) -> str:
    """'e5f0-xlang' -> 'e5f0', 'e5-off' -> 'e5': the scene's layout; the suffix names a condition built on the same
    scenes (alias_pointer_v1's languages, pointer_v2's item types), so conditions are sampled on the same scenes."""
    return level.split("-")[0]


def drop_unaligned(items: dict[str, list[dict]], tok) -> tuple[dict[str, list[dict]], dict[str, int]]:
    """Items whose alt and control prompts are not token-aligned under this target's tokenizer (prepare's asserts;
    every generator checks alignment with Qwen3.6-27B's tokenizer, another target's may split a cue differently) are
    dropped with their whole scene, every family; returns the kept items and the dropped scenes per domain."""
    bad: set[tuple[str, str]] = set()
    for its in items.values():
        for it in its:
            try:
                prepare(it, tok)
            except AssertionError:
                bad.add((it["domain"], it["scene"]))
    kept = {k: [it for it in its if (it["domain"], it["scene"]) not in bad] for k, its in items.items()}
    return kept, dict(collections.Counter(d for d, _ in bad))


def load_items(m: dict) -> dict[str, list[dict]]:
    return {label: PV.load_file(pins.REPO_ROOT / pin["file"]) for label, pin in m["items"].items()}


def eligible_ids(comp: Path | None) -> set[tuple[str, str]] | None:
    """(set, item id) with every competence prompt right. Keyed by set too: pointer_v1's main and dev sets reuse ids."""
    if comp is None:
        return None
    ok: dict[tuple[str, str], list[bool]] = collections.defaultdict(list)
    for line in comp.read_text().splitlines():
        r = json.loads(line)
        ok[(r.get("label", "").split("/")[0] if "/" in r.get("label", "") else "", r["id"])].append(r["correct"])
    return {k for k, v in ok.items() if all(v)}


def competence_path(m: dict) -> Path | None:
    if m.get("competence_path"):
        return pins.REPO_ROOT / m["competence_path"]
    return gen(m).RESULTS / m["competence"] / "items.jsonl" if m.get("competence") else None


def sample_cases(m: dict, items: dict[str, list[dict]]) -> tuple[list[dict], dict]:
    """Per (domain, base level): up to n scenes eligible in every family and every condition of the run (pointer_v1:
    one condition per level), seed SAMPLE_SEED; every family and condition on the same scenes."""
    good = eligible_ids(competence_path(m))
    by_cell: dict[tuple[str, str], dict[tuple[str, str], dict[str, dict]]] = collections.defaultdict(dict)
    for its in items.values():
        for it in its:
            if it["family"] in m["families"] and it["domain"] in m["domains"] and it["level"] in m["levels"]:
                by_cell[(it["domain"], base_level(it["level"]))].setdefault((it["family"], it["level"]), {})[
                    it["scene"]
                ] = it

    def ok(it: dict) -> bool:
        return good is None or (m["set"], it["id"]) in good or ("", it["id"]) in good

    rng = random.Random(SAMPLE_SEED)
    cases, counts = [], {}
    for (dom, lv), cells in sorted(by_cell.items()):
        keys = [(f, x) for f in m["families"] for x in m["levels"] if (f, x) in cells]
        scenes = set.intersection(*(set(cells[k]) for k in keys))
        scenes = {sc for sc in scenes if all(ok(cells[k][sc]) for k in keys)}
        picked = rng.sample(sorted(scenes), min(m["n"], len(scenes)))
        counts[f"{dom}/{lv}"] = {"eligible_scenes": len(scenes), "sampled": len(picked)}
        cases += [cells[k][sc] for sc in picked for k in keys]
    return cases, counts


# ---- stages ---------------------------------------------------------------------------------------------------------


def stage_manifest(args) -> None:
    pins.check_run_name(args.name)
    path = RESULTS / args.name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    G = gen(args.data)
    assert args.set in G.SETS, f"{args.data} has no set {args.set!r}"
    every = {lab: f for lab, f in G.set_files(args.set).items() if f.exists()}  # '<domain>_<family>_<level>' -> file
    families = args.families or list(G.FAMILIES)
    domains = args.domains or list(G.DOMAINS)
    levels = args.levels or list(dict.fromkeys(lab.split("_", 2)[2] for lab in every))
    files = {lab: f for lab, f in every.items()
             if lab.split("_", 2)[0] in domains and lab.split("_", 2)[1] in families and lab.split("_", 2)[2] in levels}  # fmt: skip
    assert files, "no item files for these domains, families and levels"
    assert args.competence or args.no_eligibility, "--competence RUN (or --no-eligibility for a smoke)"
    comp = G.RESULTS / args.competence / "items.jsonl" if args.competence else None
    layers = args.layers or default_layers(args.layer_step)
    roles = tuple(args.family_roles) if args.family_roles else FAMILY_ROLES.get(args.data, DEFAULT_ROLES)
    root = pins.REPO_ROOT
    m = {
        "exp": EXP, "run": args.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": args.why,
        "model": pins.model_pin(), "data": args.data, "set": args.set, "levels": levels, "families": families,
        "domains": domains, "family_roles": list(roles),
        # a smoke's items may live outside the repo (pointer_v4's BJ_POINTER_V4_DATA): absolute paths then
        "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                  for k, f in files.items()},
        "ci": CI_BY_DATA.get(args.data, {"kind": "wilson"}),
        "competence": args.competence,
        "competence_path": str(comp.relative_to(pins.REPO_ROOT)) if comp else None,
        "competence_sha256": sha256_of(comp) if comp else None,
        "n": args.n, "layers": layers, "control_stride": args.control_stride, "windows": default_windows(),
        "groups": args.groups or list(GROUPS), "question_max_layer": args.question_max_layer,
        "control_levels": args.control_levels, "sources": list(SOURCES), "primary_layers": args.primary_layers,
        "sample": f"per (domain, base level), up to n scenes eligible (every competence prompt right, keyed by set and "
        f"item id) in all of the run's families and conditions, seed {SAMPLE_SEED}; all of them on the same scenes",
        "seeds": {"sample": SAMPLE_SEED, "null": NULL_SEED, "other": OTHER_SEED},
        "decision": (__doc__ or "").split("Decision rule")[1].split("Stages:")[0].strip(),
    }  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def check_inputs(m: dict) -> None:
    chat.check_format(m)  # the run renders its prompts in the manifest's format (BJ_FORMAT)
    for f, pin in m["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    comp = competence_path(m)
    if comp is not None:
        assert sha256_of(comp) == m["competence_sha256"], "the competence run changed since the manifest"


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} has results; runs are written once"
    check_inputs(m)
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    items, unaligned = drop_unaligned(load_items(m), tok)
    cases, counts = sample_cases(m, items)
    counts["unaligned_scenes"] = unaligned
    print(json.dumps(counts), flush=True)
    # (family, base level) -> items, for 'other' (another domain's item of the same family and layout)
    pool: dict[tuple[str, str, str], list[dict]] = collections.defaultdict(list)
    for its in items.values():
        for it in its:  # the same answer kind too: a digit prompt ends with the space token, a word prompt does not
            pool[(it["family"], base_level(it["level"]), answer_kind(it))].append(it)
    groups = m.get("groups", list(GROUPS))
    q_max = m.get("question_max_layer")
    ctrl_levels = m.get("control_levels")

    def skip(grp: str, layer_set: list[int]) -> bool:  # the question words are patched only up to q_max
        return q_max is not None and grp in ("question", "both") and max(layer_set) > q_max

    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    layers, windows, stride = m["layers"], m["windows"], m["control_stride"]
    mid = layers[len(layers) // 2]
    record = tuple(sorted(set(layers) | {la for w in windows.values() for la in w} | {0}))
    outcomes: list[dict] = []
    checks: list[dict] = []
    for ci, c in enumerate(progress(cases, "cases")):
        prep = prepare(c, tok)
        rng = random.Random(OTHER_SEED * 1_000_003 + ci)
        kind = answer_kind(c)
        other = rng.choice(
            [o for o in pool[(c["family"], base_level(c["level"]), kind)] if o["domain"] != c["domain"]] or [c]
        )
        controls = ctrl_levels is None or c["level"] in ctrl_levels
        o_ids = S.ids(tok, prompt_text(tok, other["context"], other["question"])) + (
            S.ids(tok, " ") if kind == "digit" else []
        )
        # top token -> answer: any digit for digit items; for word items the first token of each word the item uses
        words = {str(v) for v in c["digits"]} | {v for v in c["sources"]["dissoc"]["predictions"].values() if v != "-"}
        answer_of = digit_tok if kind == "digit" else {S.answer_token(tok, w, "word"): w for w in words}
        runs = {k: model.run(torch.tensor([v], device="cuda"), record=record) for k, v in prep["read_ids"].items()}
        runs["other"] = model.run(torch.tensor([o_ids], device="cuda"), record=record)
        h = {k: v[1] for k, v in runs.items()}
        lookup = c["family"] != "RR"
        preds = c["sources"]["dissoc"]["predictions"]
        roles = role_map(c, preds, lookup)
        o_preds = other_predictions(c, other)
        o_roles = role_map(c, o_preds, lookup)
        g = prep["groups"]
        n_base, n_o = len(prep["read_ids"]["base"]), len(o_ids)

        def at(src: str, pos: list[int], shift: dict[str, int] = prep["shift"]) -> list[int]:
            return [i + shift[src] for i in pos]  # the source's positions for the base's (aligned from the end)

        jobs: list[tuple[dict, dict]] = [
            ({"layer": -1, "group": "-", "source": "unedited"}, {}),
            ({"layer": mid, "group": "both", "source": "self"}, {mid: SetRows(h["base"][mid][g["both"]], g["both"])}),
        ]
        if not prep["shift"]["dissoc"]:  # the layer-0 all-position check needs a source of the base's length
            jobs.append(({"layer": 0, "group": "all", "source": "dissoc"}, {0: SetRows(h["dissoc"][0], g["all"])}))
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 7919 * ci)
        for li, la in enumerate(layers):
            for grp in groups:
                if skip(grp, [la]):
                    continue
                pos = g[grp]
                for src in ("dissoc", "same"):
                    jobs.append(
                        ({"layer": la, "group": grp, "source": src}, {la: SetRows(h[src][la][at(src, pos)], pos)})
                    )
                if li % stride or not controls:
                    continue
                delta = h["dissoc"][la][at("dissoc", pos)] - h["base"][la][pos]
                jobs.append(({"layer": la, "group": grp, "source": "rand"}, {la: AddRows(null_rows(delta, gen), pos)}))
                pos_o = [n_o - (n_base - i) for i in pos]
                if min(pos_o) >= 0:
                    d_o = h["other"][la][pos_o] - h["base"][la][pos]
                    d_o = torch.nn.functional.normalize(d_o, dim=-1) * delta.norm(dim=-1, keepdim=True)
                    jobs.append(({"layer": la, "group": grp, "source": "other"}, {la: AddRows(d_o, pos)}))
        for wname, wl in windows.items():
            for grp in groups:
                if skip(grp, wl):
                    continue
                pos = g[grp]
                for src in ("dissoc", "same"):
                    edits = {la: SetRows(h[src][la][at(src, pos)], pos) for la in wl}
                    jobs.append(({"layer": wname, "group": grp, "source": src}, edits))
        read_ids = torch.tensor([prep["read_ids"]["base"]], device="cuda")
        wording = wording_of(c)
        logits_unedited = None
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            _, logits = model.generate_batch(read_ids, 1, [e for _, e in chunk], first_logits=True)
            logp = logits.log_softmax(-1)
            for row, (tags, _) in enumerate(chunk):
                top = int(logits[row].argmax())
                digit = answer_of.get(top)  # a digit, or (word items) one of the item's words
                rm, pr = (o_roles, o_preds) if tags["source"] == "other" else (roles, preds)
                role = rm.get(digit, "other_digit") if digit is not None else "other"
                p = {
                    h_: round(float(logp[row, S.answer_token(tok, v, kind)].exp()), 4)
                    for h_, v in pr.items()
                    if v != "-"
                }
                outcomes.append({"family": c["family"], "domain": c["domain"], "level": c["level"], "name": c["id"],
                                 "n_entities": c["n_entities"], "slot": slot_class(c), "entity": c["query"], **wording,
                                 **tags, "top": tok.decode([top]), "role": role, "p": p})  # fmt: skip
                if tags["source"] == "unedited":
                    logits_unedited = logits[row].clone()
                elif tags["source"] == "self":
                    assert logits_unedited is not None
                    checks.append({"name": c["id"], "check": "self_noop", "same_top": top == int(logits_unedited.argmax()),
                                   "max_abs_dlogit": round(float((logits[row] - logits_unedited).abs().max()), 4)})  # fmt: skip
                elif tags["group"] == "all":
                    src_logits = runs["dissoc"][0]
                    checks.append({"name": c["id"], "check": "layer0_all_reproduces_source",
                                   "same_top": top == int(src_logits.argmax()),
                                   "max_abs_dlogit": round(float((logits[row] - src_logits).abs().max()), 4)})  # fmt: skip
    write_jsonl(out_dir / "cases.jsonl", [{"id": c["id"], "family": c["family"], "domain": c["domain"],
                                           "level": c["level"]} for c in cases])  # fmt: skip
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    write_jsonl(out_dir / "checks.jsonl", checks)
    summary = summarise(outcomes, checks, m)
    summary |= {"counts": counts, "seconds": round(time.time() - t0), "edited_reads": len(outcomes)}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(name, summary))
    print((out_dir / "summary.md").read_text())


# ---- summaries ------------------------------------------------------------------------------------------------------


def cell_rates(rows: list[dict]) -> dict[str, Any]:
    n = len(rows)
    roles = collections.Counter(r["role"] for r in rows)
    return {"n": n, **{k: [round(x, 4) for x in wilson(roles[k], n)] for k in ROLES if roles[k] or k in PV.HYPOTHESES}}


def verdict(
    fam: str,
    d: dict,
    same: dict | None,
    chance: dict[str, float],
    n_ent: int,
    cands: tuple[str, ...] | None = None,
    n_free: int | None = None,
) -> str:
    """The docstring's decision rule for one cell. `cands`: the outcomes the cell's items predict (default pointer_v1's:
    identity, position, value; RR without value); `n_free`: the context digits no hypothesis predicts (default N - 3)."""
    if not d or not d["n"]:
        return "no data"
    # the cell's own 'changed' interval when it has one (analyze; pointer_v4: the cluster bootstrap), else Wilson
    changed = d.get("changed") or wilson(d["n"] - round(d["none"][0] * d["n"]), d["n"])
    if same is not None and same["n"]:
        same_changed = same.get("changed") or wilson(same["n"] - round(same["none"][0] * same["n"]), same["n"])
        if same_changed[2] > DAMAGE_MAX:
            return "damage"
    if changed[1] < CHANGED_MIN:
        return "none"
    if cands is None:
        cands = ("identity", "position") if fam == "RR" else ("identity", "position", "value")
    ctx = d.get("context", [0.0, 0.0, 0.0])
    free = n_ent - 3 if n_free is None else n_free
    per_digit = ctx[2] / free if free > 0 else 0.0
    for x in cands:
        others = [d[y][2] for y in cands if y != x]
        bar = max(chance.get(x, 0.0), per_digit)
        if d[x][1] > max(others) and d[x][1] > bar:
            return x
    return "mixed"


def summarise(outcomes: list[dict], checks: list[dict], m: dict) -> dict[str, Any]:
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    for o in outcomes:
        if o["source"] in ("unedited", "self") or o["group"] == "all":
            continue
        for dom in (o["domain"], "all"):
            cells[(o["family"], dom, o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
        if o["source"] == "dissoc":
            cells[(o["family"], f"slot_{o['slot']}", o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
    rates = {"|".join(k): cell_rates(v) for k, v in cells.items()}
    windows = m["windows"]
    verdicts: dict[str, dict[str, str]] = {}
    for key, d in rates.items():
        fam, dom, lv, grp, layer, src = key.split("|")
        if dom != "all" or src != "dissoc":
            continue
        same = rates.get("|".join((fam, dom, lv, grp, layer, "same")))
        layers = windows.get(layer, [int(layer)] if layer.lstrip("-").isdigit() else [])
        chance: dict[str, float] = {}
        for la in layers:
            r = rates.get("|".join((fam, dom, lv, grp, str(la), "rand")))
            for x in PV.HYPOTHESES:
                if r and x in r:
                    chance[x] = max(chance.get(x, 0.0), r[x][2])
        n_ent = int(lv[1])
        verdicts.setdefault(f"{fam}|{lv}|{grp}", {})[layer] = verdict(fam, d, same, chance, n_ent)
    chk: dict[str, Any] = {}
    for kind in ("self_noop", "layer0_all_reproduces_source"):
        rows = [c for c in checks if c["check"] == kind]
        if rows:
            chk[kind] = {"n": len(rows), "same_top": sum(c["same_top"] for c in rows),
                         "max_abs_dlogit_max": max(c["max_abs_dlogit"] for c in rows)}  # fmt: skip
    unedited = [o for o in outcomes if o["source"] == "unedited"]
    chk["unedited_base_answer_read"] = {"n": len(unedited), "base_answer": sum(o["role"] == "none" for o in unedited)}
    primary = {k: v.get("transit") for k, v in verdicts.items() if k.startswith("RL|") and k.endswith("|final")}
    return {"rates": rates, "verdicts": verdicts, "checks": chk, "primary_RL_final_transit": primary}


def summary_md(name: str, s: dict) -> str:
    lines = [f"# {EXP} / {name}", "", f"Checks: {json.dumps(s['checks'])}", "",
             f"Primary (RL, final, transit window): {json.dumps(s['primary_RL_final_transit'])}", "",
             "## Verdicts (dissoc, pooled over domains), per layer / window", ""]  # fmt: skip
    for k, v in s["verdicts"].items():
        lines.append(f"- {k}: " + ", ".join(f"{la}: {x}" for la, x in v.items()))
    lines += ["", "## Shares (pooled over domains): role rate [95% CI]", "",
              "| family | level | group | layer | source | n | none | identity | position | value | context | other |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for key, d in s["rates"].items():
        fam, dom, lv, grp, layer, src = key.split("|")
        if dom != "all":
            continue

        def f(r, d=d):
            x = d.get(r)
            return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f},{100 * x[2]:.0f}]" if x else "-"

        oth = sum(d[r][0] for r in ("recall", "other_digit", "other") if r in d)
        lines.append(f"| {fam} | {lv} | {grp} | {layer} | {src} | {d['n']} | {f('none')} | {f('identity')} | "
                     f"{f('position')} | {f('value')} | {f('context')} | {100 * oth:.0f}% |")  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_summarise(name: str) -> None:
    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    checks = [json.loads(x) for x in (run_dir / "checks.jsonl").read_text().splitlines()]
    out = run_dir / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    s = summarise(rows, checks, m)
    (out / "summary.json").write_text(json.dumps(s, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(name, s))
    print("wrote", out)


# ---- analysis (CPU: re-applies the pre-registered rule to a finished run, with domain and slot cuts) -----------------

# The 'same' control's Wilson upper bound at zero changes is 3.84 / (n + 3.84): <= DAMAGE_MAX only from n = 35, so a
# cell with fewer items can never be interpretable under the rule (d3_pilot_27b's "damage" everywhere).
MIN_N_RULE = 35
CUT_KINDS = ("all", "domain", "slot")
SUPERSEDED = {  # shown in figure notes and reports: plain words, no run ids
    "d3_pilot_27b": "pilot with 34 prompts per family: below 35 the rule's control bound cannot pass, so every cell "
    "reads 'damage'; includes topics that failed the competence check",
    "d3_main_27b": "includes months and planets, whose memory → prompt / memory → memory prompts fail the "
    "pre-registered competence check (months memory → prompt 46%, planets memory → memory 55%, planets memory → "
    "prompt lower bound 0.84)",
    "d3_pilot_levels_27b": "includes topics that failed the competence check and only 15 prompts per topic",
    "d3_smoke_27b": "smoke run: 1 prompt per topic, competence check skipped; a code-path and timing check, not a result",
}


def roles_of(rows: list[dict], ci: dict | None = None) -> dict[str, Any]:
    """n, role counts, (rate, lo, hi) per role and for 'changed' (any role but none): Wilson, or with `ci` of kind
    entity_cluster the entity-cluster bootstrap (asked entity within each domain) widened to Wilson where Wilson is
    wider, Wilson kept under 'wilson'. k_entities / t_wordings: distinct asked entities and wordings, where recorded."""
    n = len(rows)
    k = collections.Counter(r["role"] for r in rows)
    out: dict[str, Any] = {"n": n, "k": dict(k)}
    ents = {(r["domain"], r["entity"]) for r in rows if "entity" in r}
    words = {(r["domain"], r["template"]) for r in rows if "template" in r}
    if ents:
        out["k_entities"] = len(ents)
    if words:
        out["t_wordings"] = len(words)
    cluster = bool(ci and ci.get("kind") == "entity_cluster")
    if cluster:
        out["wilson"] = {}
    for role in (*ROLES, "changed"):
        hits = [r["role"] != "none" if role == "changed" else r["role"] == role for r in rows]
        out[role] = rate_ci(hits, rows, ci)
        if cluster:
            out["wilson"][role] = rate_ci(hits, rows, None)
    return out


def rate_ci(hits: list[bool], rows: list[dict], ci: dict | None) -> list[float]:
    """(rate, lo, hi) of per-item hits: Wilson 95%, or with `ci` of kind entity_cluster the entity-cluster bootstrap
    (rows' (domain, entity) resampled within each domain; stats.cluster_bootstrap) widened to Wilson where Wilson is
    wider (at 0 or n hits every resample agrees and the Wilson interval stands)."""
    n, h = len(hits), sum(hits)
    w = [round(x, 4) for x in wilson(h, n)]
    if not (ci and ci.get("kind") == "entity_cluster") or not 0 < h < n:
        return w
    from bridge_jspace.stats import cluster_bootstrap

    _, lo, hi = cluster_bootstrap([float(x) for x in hits], [(r["domain"], r["entity"]) for r in rows],
                                  [r["domain"] for r in rows], ci["n_boot"], ci["seed"])  # fmt: skip
    return [w[0], round(min(lo, w[1]), 4), round(max(hi, w[2]), 4)]


def newcombe(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float, float]:
    """Difference of two independent proportions with Newcombe's hybrid Wilson interval (method 10)."""
    p1, l1, u1 = wilson(k1, n1)
    p2, l2, u2 = wilson(k2, n2)
    d = p1 - p2
    return (d, d - ((p1 - l1) ** 2 + (u2 - p2) ** 2) ** 0.5, d + ((u1 - p1) ** 2 + (p2 - l2) ** 2) ** 0.5)


def analyze(m: dict, rows: list[dict], checks: list[dict]) -> dict[str, Any]:
    """Every cell (family x cut x level x group x layer/window x source) with its rates; the rule's verdict for every
    dissoc cell, flagged where n < MIN_N_RULE makes it unreachable; strongest layers; level contrasts."""
    cells: dict[tuple, list[dict]] = collections.defaultdict(list)
    for o in rows:
        if o["source"] not in SOURCES or o["group"] == "all":
            continue
        for cut in ("all", f"domain:{o['domain']}", f"slot:{o['slot']}"):
            cells[(o["family"], cut, o["level"], o["group"], str(o["layer"]), o["source"])].append(o)
    ci = m.get("ci")
    rates = {"|".join(k): roles_of(v, ci) for k, v in cells.items()}
    windows = m["windows"]
    pf, rf, cf = family_roles(m)
    # which outcomes each (family, level) predicts: the keys of the alt prompt's predictions stored with every read
    has: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    for o in rows:
        if o["source"] == "dissoc":
            has[(o["family"], o["level"])] |= set(o.get("p", {}))

    def cands_of(fam: str, lv: str) -> tuple[str, ...]:
        hs = has.get((fam, lv)) or set(PV.HYPOTHESES)
        out = [h for h in ("identity", "position", *POINTER_ROLES, "value") if h in hs]
        return tuple(h for h in out if not (fam == cf and h == "value"))

    def free_of(fam: str, lv: str) -> int:
        hs = has.get((fam, lv)) or set(PV.HYPOTHESES)
        in_ctx = [h for h in ("none", "identity", "position", *POINTER_ROLES) if h in hs] + (
            ["value"] if lv.endswith("-ref") else []
        )
        return int(lv[1]) - len(in_ctx)

    verdicts: dict[str, Any] = {}
    for key, d in rates.items():
        fam, cut, lv, grp, layer, src = key.split("|")
        if src != "dissoc":
            continue
        same = rates.get("|".join((fam, cut, lv, grp, layer, "same")))
        chance: dict[str, float] = {}
        for la in windows.get(layer, [int(layer)] if layer.lstrip("-").isdigit() else []):
            r = rates.get("|".join((fam, cut, lv, grp, str(la), "rand")))
            for x in HYPS:
                if r:
                    chance[x] = max(chance.get(x, 0.0), r[x][2])
        n_same = same["n"] if same else 0
        verdicts["|".join((fam, cut, lv, grp, layer))] = {
            "verdict": verdict(fam, d, same, chance, int(lv[1]), cands_of(fam, lv), free_of(fam, lv)),
            "n": d["n"],
            "n_same": n_same,
            "rule_reachable": min(d["n"], n_same) >= MIN_N_RULE,
            "chance_bar": chance,
        }
    single = [la for la in m["layers"]]
    strongest: dict[str, Any] = {}
    for fam in m["families"]:
        for lv in m["levels"]:
            for grp in m.get("groups", list(GROUPS)):
                cand = [
                    (rates[k]["changed"][0], la) for la in single if (k := f"{fam}|all|{lv}|{grp}|{la}|dissoc") in rates
                ]
                if not cand:
                    continue
                best = max(cand, key=lambda t: (t[0], -t[1]))[1]
                d = rates[f"{fam}|all|{lv}|{grp}|{best}|dissoc"]
                strongest[f"{fam}|{lv}|{grp}"] = {"layer": best, **{r: d[r] for r in ("changed", *HYPS)}}
    levels: dict[str, Any] = {}
    # alias_pointer_v1: each condition exists in one domain, so compare it with English in that domain only
    lv_cuts = (
        ["all"]
        if m.get("data", "pointer_v1") in ("pointer_v1", "code_pointer_v1")
        else [f"domain:{x}" for x in m["domains"]]
    )
    if "e5f0" in m["levels"] and len(m["levels"]) > 1:
        for lv in m["levels"]:
            if lv == "e5f0":
                continue
            for cut, grp in [(c_, g_) for c_ in lv_cuts for g_ in ("final", "last")]:
                a, b = (
                    rates.get(f"{pf}|{cut}|{lv}|{grp}|transit|dissoc"),
                    rates.get(f"{pf}|{cut}|e5f0|{grp}|transit|dissoc"),
                )
                if not a or not b:
                    continue
                ok = all(
                    verdicts[f"{pf}|{cut}|{x}|{grp}|transit"]["verdict"] not in ("none", "damage") for x in (lv, "e5f0")
                )
                diffs = {}
                for role in PV.HYPOTHESES:
                    dd = newcombe(a["k"].get(role, 0), a["n"], b["k"].get(role, 0), b["n"])
                    label = (
                        "same"
                        if dd[1] >= -0.15 and dd[2] <= 0.15
                        else "differs"
                        if (dd[1] > 0 or dd[2] < 0) and abs(dd[0]) > 0.15
                        else "unclear"
                    )
                    diffs[role] = {"diff": [round(x, 4) for x in dd], "label": label}
                levels[f"{lv}_vs_e5f0|{grp}" if cut == "all" else f"{lv}_vs_e5f0|{cut}|{grp}"] = {
                    "interpretable": ok,
                    "diffs": diffs,
                }
    chk: dict[str, Any] = {}
    for kind in ("self_noop", "layer0_all_reproduces_source"):
        cr = [c for c in checks if c["check"] == kind]
        if cr:
            chk[kind] = {"n": len(cr), "same_top": sum(c["same_top"] for c in cr),
                         "max_abs_dlogit_max": max(c["max_abs_dlogit"] for c in cr)}  # fmt: skip
    unedited = [o for o in rows if o["source"] == "unedited"]
    chk["unedited_base_answer_read"] = {"n": len(unedited), "base_answer": sum(o["role"] == "none" for o in unedited)}
    unreachable = sorted(k for k, v in verdicts.items() if not v["rule_reachable"])
    return {
        "run": m["run"],
        "superseded": SUPERSEDED.get(m["run"]),
        "levels": m["levels"],
        "domains": sorted({o["domain"] for o in rows}),
        "n_per_family": {
            f"{f}|{lv}": rates[f"{f}|all|{lv}|final|transit|dissoc"]["n"]
            for f in m["families"]
            for lv in m["levels"]
            if f"{f}|all|{lv}|final|transit|dissoc" in rates
        },
        # n items / k asked entities / t wordings of the same cells (k, t: 0 where the items do not record them)
        "nkt_per_family": {
            f"{f}|{lv}": [
                (c := rates[f"{f}|all|{lv}|final|transit|dissoc"])["n"],
                c.get("k_entities", 0),
                c.get("t_wordings", 0),
            ]
            for f in m["families"]
            for lv in m["levels"]
            if f"{f}|all|{lv}|final|transit|dissoc" in rates
        },
        "ci": m.get("ci", {"kind": "wilson"}),
        "checks": chk,
        "family_roles": [pf, rf, cf],
        "predicted": {lv: sorted({h for (f, x), hs in has.items() if x == lv for h in hs}) for lv in m["levels"]},
        "primary": {
            lv: {
                "verdict": verdicts.get(f"{pf}|all|{lv}|final|transit", {}),
                "rates": rates.get(f"{pf}|all|{lv}|final|transit|dissoc"),
            }
            for lv in m["levels"]
        },
        "ref_contrasts": ref_contrasts(m, rows, verdicts),
        "v4x": v4x_tests(m, rates) if m.get("data") == "pointer_v4x" else {},
        "v6": v6_tests(m, rates) if m.get("data") == "pointer_v6" else {},
        "v5": v5_tests(m, verdicts) if m.get("data") == "pointer_v5" else {},
        "strongest_layer": strongest,
        "level_contrasts": levels,
        "verdicts": verdicts,
        "rule_unreachable_cells": {"count": len(unreachable), "cuts": sorted({k.split("|")[1] for k in unreachable})},
        "rates": rates,
    }


def v4x_tests(m: dict, rates: dict) -> dict[str, Any]:
    """pointer_v4x's pre-registered tests (the docstring's pointer_v4x additions): per level, primary layer and cut
    (pooled, each topic), whether the winner's lower bound exceeds each rival's upper bound; then H-order-v4 (e5-off)
    and H-start-v4 (e5more and e5fewer): true pooled and in >= 2 of 3 topics at the same primary layer (the 27B: 48 or
    50)."""
    pf = family_roles(m)[0]
    layers = primary_layers(m)
    cells: dict[str, Any] = {}
    for lv, (win, rivals) in V4X_TESTS.items():
        if lv not in m["levels"]:
            continue
        for la in layers:
            for cut in ["all", *(f"domain:{d}" for d in m["domains"])]:
                d = rates.get(f"{pf}|{cut}|{lv}|last|{la}|dissoc")
                if not d:
                    continue
                beats = d[win][1] > max(d[r][2] for r in rivals)
                cells[f"{lv}|{la}|{cut}"] = {"n": d["n"], "k_entities": d.get("k_entities"), "winner": d[win],
                                             **{r: d[r] for r in rivals}, "beats": beats,
                                             "reachable": d["n"] >= MIN_N_RULE}  # fmt: skip

    def holds(levels: tuple[str, ...]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for la in layers:
            ok = True
            for lv in levels:  # a cut counts only if it passes and has the n the rule needs (>= MIN_N_RULE)

                def ok_cut(cut: str, lv: str = lv, la: str = la) -> bool:
                    c = cells.get(f"{lv}|{la}|{cut}", {})
                    return bool(c.get("beats")) and bool(c.get("reachable"))

                pooled = ok_cut("all")
                topics = sum(ok_cut(f"domain:{d}") for d in m["domains"])
                ok = ok and pooled and topics >= 2
                out[f"{lv}|{la}"] = {"pooled": pooled, "topics": topics}
            out[f"layer {la}"] = ok
        out["holds"] = any(out[f"layer {la}"] for la in layers)
        return out

    return {"cells": cells, "H-order-v4": holds(("e5-off",)), "H-start-v4": holds(("e5more", "e5fewer"))}


def v5_tests(m: dict, verdicts: dict) -> dict[str, Any]:
    """pointer_v5's pre-registered tests (the docstring's pointer_v5 additions): per level, the rule's verdict at the
    last two tokens, memory -> prompt, each primary layer: "same statement slot" pooled and in >= 2 of 3 topics (cells
    with n >= 35)."""
    pf = family_roles(m)[0]
    out: dict[str, Any] = {}
    for lv in m["levels"]:
        layers: dict[str, Any] = {}
        for la in primary_layers(m):
            pooled = verdicts.get(f"{pf}|all|{lv}|last|{la}", {})
            topics = [
                d
                for d in m["domains"]
                if (v := verdicts.get(f"{pf}|domain:{d}|{lv}|last|{la}", {})).get("verdict") == "position"
                and v.get("rule_reachable")
            ]
            ok = pooled.get("verdict") == "position" and bool(pooled.get("rule_reachable")) and len(topics) >= 2
            layers[la] = {"pooled": pooled.get("verdict"), "topics_with_slot": topics, "holds": ok}
        out[lv] = {"layers": layers, "holds": any(c["holds"] for c in layers.values())}
    return out


V6_LEVELS = ("e5-still", "e5-abs", "e5-rel", "e5-long")


def v6_tests(m: dict, rates: dict) -> dict[str, Any]:
    """pointer_v6's pre-registered tests (the docstring's pointer_v6 additions): memory -> prompt, the last two tokens,
    each primary layer, pooled. Differences between levels: Newcombe intervals on items (the levels share their scenes,
    so treating them as independent is conservative)."""
    pf = family_roles(m)[0]
    layers: dict[str, Any] = {}
    for la in primary_layers(m):
        still, ab, rel, long = (rates.get(f"{pf}|all|{lv}|last|{la}|dissoc") for lv in V6_LEVELS)
        c: dict[str, Any] = {}
        if ab and rel:

            def diff(x: dict, rx: str, y: dict, ry: str) -> list[float]:
                return [round(v, 4) for v in newcombe(x["k"].get(rx, 0), x["n"], y["k"].get(ry, 0), y["n"])]

            c = {"n": [ab["n"], rel["n"]], "moved_abs": ab["token"], "moved_rel": rel["back"],
                 "rel_minus_abs": diff(rel, "back", ab, "token"), "slot_abs": ab["position"], "slot_rel": rel["position"],
                 "slot_abs_minus_rel": diff(ab, "position", rel, "position"),
                 "ordinal": {"abs": ab["position"][1] > ab["token"][2], "rel": rel["position"][1] > rel["back"][2]},
                 "reachable": min(ab["n"], rel["n"]) >= MIN_N_RULE}  # fmt: skip
            if still and long:
                c |= {"slot_still": still["position"], "slot_long": long["position"],
                      "long_minus_still": diff(long, "position", still, "position"),
                      "word_long_minus_still": diff(long, "identity", still, "identity")}  # fmt: skip
        layers[la] = c

    def any_layer(test) -> bool:
        return any(c and c["reachable"] and test(c) for c in layers.values())

    return {
        "layers": layers,
        "H-rel": any_layer(lambda c: c["rel_minus_abs"][1] > 0),
        "H-abs": any_layer(lambda c: c["rel_minus_abs"][2] < 0),
        "H-ordinal": any_layer(lambda c: c["ordinal"]["abs"] and c["ordinal"]["rel"]),
        "H-long": any_layer(lambda c: "long_minus_still" in c and c["long_minus_still"][2] < 0),
    }


REF_MARGIN = 0.10


def ref_contrasts(m: dict, rows: list[dict], verdicts: dict) -> dict[str, Any]:
    """pointer_v2's reflexive test: per family x group x layer/window, the paired difference of the 'value' share between
    the e<N>-ref and e<N>-pln items of the same scene (the docstring's v2 rule)."""
    from bridge_jspace.stats import paired_bootstrap_diff

    pairs = [(lv, lv[: -len("-ref")] + "-pln") for lv in m["levels"] if lv.endswith("-ref")]
    pairs = [(r, p) for r, p in pairs if p in m["levels"]]
    out: dict[str, Any] = {}
    if not pairs:
        return out
    val: dict[tuple, dict[str, float]] = collections.defaultdict(dict)
    for o in rows:
        if o["source"] == "dissoc" and o["group"] != "all":
            scene = o["name"].replace(f"-{o['level']}-", "-")
            val[(o["family"], o["level"], o["group"], str(o["layer"]))][scene] = float(o["role"] == "value")
    for ref, pln in pairs:
        for (fam, lv, grp, layer), a in val.items():
            if lv != ref:
                continue
            b = val.get((fam, pln, grp, layer), {})
            names = sorted(set(a) & set(b))
            if not names:
                continue
            d = paired_bootstrap_diff([a[x] for x in names], [b[x] for x in names], 2000, 0)
            label = ("reflexive" if d[1] > REF_MARGIN else "value" if d[1] >= -REF_MARGIN and d[2] <= REF_MARGIN
                     else "unclear")  # fmt: skip
            pv = verdicts.get(f"{fam}|all|{pln}|{grp}|{layer}", {})
            out[f"{fam}|{ref}|{grp}|{layer}"] = {
                "n_pairs": len(names), "ref_value": round(sum(a[x] for x in names) / len(names), 4),
                "pln_value": round(sum(b[x] for x in names) / len(names), 4), "diff": [round(x, 4) for x in d],
                "label": label, "interpretable": pv.get("verdict") not in (None, "none", "damage"),
            }  # fmt: skip
    return out


def load_run(name: str) -> tuple[dict, list[dict], list[dict]]:
    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    checks = [json.loads(x) for x in (run_dir / "checks.jsonl").read_text().splitlines()]
    return m, rows, checks


def stage_analyze(name: str) -> Path:
    m, rows, checks = load_run(name)
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-rule"
    out.mkdir()
    a = analyze(m, rows, checks)
    (out / "summary.json").write_text(json.dumps(a, indent=1) + "\n")
    print("wrote", out)
    return out


def near_ties(rows: list[dict], gap: float = 0.1) -> dict[str, Any]:
    """Among dissoc reads whose top token is a predicted digit, the share where the runner-up prediction's p is within
    `gap` of the winner's (bf16 batch noise could flip those)."""
    win = [o for o in rows if o["source"] == "dissoc" and o["role"] in HYPS and o["group"] != "all"]
    close = 0
    for o in win:
        ps = sorted({o["p"].get(h, 0.0) for h in HYPS if h in o["p"]}, reverse=True)
        close += len(ps) > 1 and ps[0] - ps[1] < gap
    return {"n": len(win), "within_gap": close, "gap": gap}


# ---- figures (CPU) --------------------------------------------------------------------------------------------------

# Outcome hues: the reference categorical palette's first three slots (validated: adjacent CVD dE >= 9.2, normal-vision
# >= 27.6 on the light surface; aqua is below 3:1 contrast, so lines carry direct labels). 'none' and every control are
# grey: they are baselines, not identities.
OUTCOME_COLOR = {"identity": "#2a78d6", "position": "#eb6834", "value": "#1baf7a", "token": "#eda100", "end": "#6250d6",
                 "back": "#e87ba4"}  # fmt: skip
NONE_COLOR = "#52514e"
CONTROL_STYLE = {
    "same": ("#898781", (0, (4, 2))),
    "rand": ("#898781", (0, (1, 1.6))),
    "other": ("#b5b3aa", (0, (6, 2, 1, 2))),
}
# Display terms for an outside reader (figure_terms.md, 2026-10-21): org prompt = the base, alt prompt = the source,
# bridge alt = the entity the alt prompt asks about.
OUTCOME_TERM = {
    "identity": "answer of bridge alt's statement",
    "position": "answer at the same statement slot",
    "end": "answer at the same slot counted from the end",
    "token": "answer at the same token position",
    "back": "answer at the same distance back from the question",
    "value": "the alt prompt's own answer",
    "none": "answer org kept",
}
OUTCOME_SHORT = {
    "identity": "bridge alt's statement",
    "position": "same slot",
    "end": "same slot from the end",
    "token": "same token position",
    "back": "same distance back",
    "value": "alt prompt's answer",
}
GROUP_SHORT = {
    "question": "question words",
    "final": "after the question",
    "last": "last 2 tokens",
    "both": "question + after",
}
OUTCOME_HELP = {
    "identity": "org prompt's digit for bridge alt",
    "position": "org prompt's digit in bridge alt's slot",
    "end": "the same, counted from the end",
    "token": "org prompt's digit at bridge alt's token offset",
    "back": "org prompt's digit as many tokens before the question as bridge alt's",
    "value": "the alt prompt's answer",
    "none": "",
}
CONTROL_LABEL = {
    "same": "control: same entity, statements reshuffled (% changed)",
    "rand": "control: random push, same size (% changed)",
    "other": "control: another topic's prompt, same size (% changed)",
}
GROUP_TITLE = {
    "question": "question words",
    "final": "everything after the question",
    "last": "last two tokens before the answer",
    "both": "question words + everything after",
}
FAMILY_TITLE = {  # display names (the user's rule: never the letter codes): where the bridge comes from -> the answer
    "RL": "memory → prompt (recalled cue, prompt lookup)",
    "DL": "named → prompt (entity named, prompt lookup)",
    "RR": "memory → memory (recalled cue, recalled fact)",
}
_CODE_RE = re.compile(r"(?<![\w|/`=-])(BLR|BRL|CH2|CH3|RL|RR|DL|BL|BR|DK|IX|RK)(?![\w|/`-])")


def family_label(code: str) -> str:
    """Display name of a family code (plotting.FAMILY_LABEL, then code_pointer_v1's)."""
    from bridge_jspace.plotting import FAMILY_LABEL

    if code in FAMILY_LABEL:
        return FAMILY_LABEL[code]
    from scripts import code_pointer_v1 as CP

    return CP.FAMILY_LABEL.get(code, code)


def fam_title(fam: str) -> str:
    return FAMILY_TITLE.get(fam, family_label(fam))


def is_code(m: dict) -> bool:
    return m.get("data") == "code_pointer_v1"


def level_text(m: dict, lv: str) -> str:
    names = {"e3f0": "3 statements", "e5f0": "5 statements", "e5f4": "5 statements with filler sentences between them"}
    if lv in names and is_code(m):
        return names[lv].replace("statements", "dict entries")
    if lv in names and m.get("data", "pointer_v1") == "pointer_v1":
        return names[lv]
    G = gen(m)
    return G.level_name(lv) if hasattr(G, "level_name") else f"{int(lv[1])} statements"


def plain(text: str) -> str:
    """Family codes replaced by their display names, outside `code spans` (data keys keep their codes there)."""
    words = (("base's residual", "org prompt's hidden states"), ("dissoc source's", "alt prompt's"),
             ("the dissoc source", "the alt prompt"), ("dissoc", "alt prompt"),
             ("the 'same' control", "the same-entity control (statements reshuffled)"),
             ("'same' control", "same-entity control"), ("'same' changes", "same-entity control changes"),
             ("the same control", "the same-entity control (statements reshuffled)"),
             ("same control", "same-entity control"), ("the rand control", "the random-push control"),
             ("rand control", "random-push control"), ("random-direction control", "random-push control"),
             ("random direction changed", "random push of the same size changed"),
             ("other item changed", "another domain's prompt changed"), ("| same n |", "| control n |"),
             ("a single 'same' change", "a single same-entity-control change"))  # fmt: skip
    fence = "\x00FENCE\x00"  # ``` fences are not code spans: keep them out of the backtick parity
    parts = text.replace("```", fence).split("`")
    for i in range(0, len(parts), 2):
        parts[i] = _CODE_RE.sub(lambda mm: family_label(mm.group(1)), parts[i])
        for old, new in words:
            parts[i] = parts[i].replace(old, new)
    return "`".join(parts).replace(fence, "```")


VERDICT_TERM = {
    "identity": "bridge alt's statement (H-word)",
    "position": "same statement slot (H-pointer)",
    "value": "alt prompt's own answer (H-value)",
    "none": "no effect",
    "mixed": "mixed",
    "damage": "damage",
    "no data": "no data",
}


def rule_plain(text: str) -> str:
    """The pre-registered rule with its outcome names in the outside reader's terms (the variable X renamed W)."""
    text = re.sub(r"\bX\b", "W", text)
    for old, new in (("identity", OUTCOME_TERM["identity"]), ("position", OUTCOME_TERM["position"]),
                     ("value", OUTCOME_TERM["value"]), ("share none", f"share '{OUTCOME_TERM['none']}'")):  # fmt: skip
        text = re.sub(rf"\b{old}\b", new, text)
    return text


def example_line(m: dict, name: str, level: str | None = None) -> str:
    """One shortened prompt pair in outside-reader terms, from the run's examples.json: a memory → prompt item (of
    `level`, if given) whose patch gave the same-slot answer, else another of that level, else the first example."""
    ex = RESULTS / name / "examples.json"
    if not ex.exists():
        return ""
    e = json.loads(ex.read_text())["examples"]
    at = [x for x in e if level is None or f"-{level}-" in x["item_id"]] or e
    pf = family_roles(m)[0]
    pick = (next((x for x in at if x["family"] == pf and x["group"] == "position"), None)
            or next((x for x in at if x["family"] == pf), None) or (at[0] if at else None))  # fmt: skip
    if not pick:
        return ""
    it = next((i for its in load_items(m).values() for i in its if i["id"] == pick["item_id"]), None)
    if not it:
        return ""
    d, sl = it["sources"]["dissoc"], it["slots"]
    k = sl["position"]
    nth = {0: "1st", 1: "2nd", 2: "3rd"}.get(k, f"{k + 1}th")
    exp = d["predictions"]
    shown = sorted({j for j in (sl["query"], sl.get("identity"), k, sl.get("token"), sl.get("back"),
                                sl.get("value_in_org")) if isinstance(j, int)})  # fmt: skip
    if "statements" in it:  # alias_pointer_v1 records each prompt's statements
        org = " ... ".join(it["statements"][j] for j in shown)
    elif it["domain"] in PV.DOMAINS and m.get("data", "pointer_v1") in ("pointer_v1", "pointer_v2", "pointer_v3"):
        stmt = PV.DOMAINS[it["domain"]]["statement"]
        org = " ... ".join(stmt.format(e=it["entities"][j], d=it["digits"][j]) for j in shown)
    else:  # code: the context is a program; show its last line before the query
        org = it["context"].strip().splitlines()[-1]
    question = " ".join(it["question"].replace("```", " ").split())  # code: no fences or line breaks in a caption
    term = dict(OUTCOME_TERM)
    if isinstance(sl.get("value_in_org"), int):
        term["value"] += ", also in the org prompt"
    if exp.get("end", "-") != "-":
        term["position"] = "answer at the same slot counted from the start"
    opts = ", ".join(f"{exp[h]} ({term[h]})" for h in ("identity", "position", *POINTER_ROLES, "value", "none")
                     if exp.get(h, "-") != "-")  # fmt: skip
    return (
        f'org prompt "... {org} ... {question}" -> answer org {exp["none"]}; the alt prompt asks about the '
        f"{d['query']} (bridge alt), its {nth} statement. Possible answers after the patch: {opts}."
    )


def _series(
    a: dict, prefix: str, layers: list[int], src: str, role: str
) -> tuple[list[int], list[float], list[float], list[float]]:
    xs, r, lo, hi = [], [], [], []
    for la in layers:
        d = a["rates"].get(f"{prefix}|{la}|{src}")
        if d:
            xs.append(la)
            r.append(d[role][0])
            lo.append(max(0.0, d[role][1]))
            hi.append(d[role][2])
    return xs, r, lo, hi


def band_words() -> str:
    """What the grey band (the transit window) marks: on the 27B, where the lens reads the bridge but cannot steer it;
    on another target, the same relative depth (WINDOW_FRACTIONS), with no lens claim."""
    if pins.TARGET == "qwen3.6-27b":
        return "the lens reads the bridge but cannot steer it"
    return "the 27B's layers 44-52 at the same relative depth"


def _band(ax, lo: int, hi: int, text: str | None) -> None:
    from bridge_jspace.plotting import GRID, MUTED

    ax.axvspan(lo, hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    if text:
        ax.annotate(text, ((lo + hi) / 2, 1), xycoords=("data", "axes fraction"), xytext=(0, -3),
                    textcoords="offset points", ha="center", va="top", fontsize=7, color=MUTED)  # fmt: skip


def _panel(
    ax, a: dict, m: dict, fam: str, cut: str, lv: str, grp: str, controls=("same", "rand", "other"), band=True
) -> int:
    """Outcome shares by layer for one cell, with Wilson bands, the 'none' share, and each control's change rate."""
    from bridge_jspace.plotting import percent_axis, style_axes

    style_axes(ax)
    layers = sorted(m["layers"])
    prefix = f"{fam}|{cut}|{lv}|{grp}"
    tr = m["windows"]["transit"]
    if band:
        _band(ax, tr[0], tr[-1], None)  # labelled once, in the legend
    n = 0
    cf = family_roles(m)[2]
    roles = [h for h in ("identity", "position", *POINTER_ROLES, "value") if not (fam == cf and h == "value")]
    roles = [
        h for h in roles if (h != "token" or has_token(a, lv)) and (h not in ("end", "back") or has_role(a, lv, h))
    ]
    for role in roles:
        xs, r, lo, hi = _series(a, prefix, layers, "dissoc", role)
        if not xs:
            continue
        near = [r[j] > 0 or (j > 0 and r[j - 1] > 0) or (j + 1 < len(r) and r[j + 1] > 0) for j in range(len(r))]
        ax.fill_between(xs, lo, hi, where=near, color=OUTCOME_COLOR[role], alpha=0.14, lw=0)
        ax.plot(xs, r, color=OUTCOME_COLOR[role], lw=2, solid_capstyle="round")
    xs, r, _, _ = _series(a, prefix, layers, "dissoc", "none")
    ax.plot(xs, r, color=NONE_COLOR, lw=1.1)
    for src in controls:
        xs, r, _, _ = _series(a, prefix, layers, src, "changed")
        if xs:
            col, ls = CONTROL_STYLE[src]
            ax.plot(xs, r, color=col, lw=1.2, ls=ls, marker="o" if src != "same" else None, ms=2.5)
    d = a["rates"].get(f"{prefix}|{layers[0]}|dissoc")
    n = d["n"] if d else 0
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlim(layers[0] - 1, layers[-1] + 1)
    percent_axis(ax)
    return n


def _handles(
    fams: list[str], controls=("same", "rand", "other"), token: bool = False, end: bool = False, back: bool = False
) -> list:
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace.plotting import GRID

    term = dict(OUTCOME_TERM)
    if end:  # with an end-counted slot in the figure, say which way the plain slot is counted
        term["position"] = "answer at the same slot counted from the start"
    h: list[Any] = [Line2D([], [], color=OUTCOME_COLOR[r], lw=2,
                label=f"% that become {term[r].removeprefix('the ')} ({OUTCOME_HELP[r]})")
         for r in ("identity", "position", *(("end",) if end else ()), *(("token",) if token else ()),
                   *(("back",) if back else ()), "value")]  # fmt: skip
    h.append(Line2D([], [], color=NONE_COLOR, lw=1.1, label="% of original answers kept (answer org kept)"))
    tr = default_windows()["transit"]
    h.append(Patch(color=GRID, alpha=0.7, lw=0, label=f"layers {tr[0]}-{tr[-1]}: {band_words()}"))
    for src in controls:
        col, ls = CONTROL_STYLE[src]
        h.append(
            Line2D(
                [],
                [],
                color=col,
                lw=1.2,
                ls=ls,
                marker="o" if src != "same" else None,
                ms=2.5,
                label=CONTROL_LABEL[src],
            )
        )
    return h


def _finish(fig, path: Path, title: str, rows: list[tuple[str, str]], handles: list, ncols: int = 2) -> list[str]:
    """plotting.finish's frame with its labelled caption rows (What we did / Example / How to read / Control / Data),
    legend below; saved as PNG at 200 dpi and as SVG (plotting.finish saves one PNG at 150 dpi)."""
    import textwrap

    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK, MUTED, SURFACE

    h, w = fig.get_figheight(), fig.get_figwidth()
    label_w = 1.05
    # the title wrapped like the caption rows (~11 characters per inch at 12 pt): it never runs off the right edge
    title_lines = textwrap.wrap(title, width=int((w - 0.2) * 11)) or [""]
    wrapped = [(label, textwrap.wrap(text, width=int((w - label_w - 0.2) * 15.5)) or [""]) for label, text in rows]
    y0 = 0.38 + 0.21 * (len(title_lines) - 1)
    head = y0 + sum(0.155 * len(lines) + 0.05 for _, lines in wrapped) + 0.1
    n_rows = -(-len(handles) // ncols)
    foot = 0.2 + 0.25 * n_rows
    # callers budget 1.6 in for caption and legend; a longer caption grows the figure instead of squeezing the panels
    h = max(h, h - 1.6 + head + foot)
    fig.set_figheight(h)
    fig.text(0.01, 1 - 0.1 / h, "\n".join(title_lines), ha="left", va="top", fontsize=12, color=INK, linespacing=1.25)
    y = y0
    for label, lines in wrapped:
        fig.text(0.01, 1 - y / h, label, ha="left", va="top", fontsize=8.5, color=INK, fontweight="bold")
        fig.text(
            label_w / w, 1 - y / h, "\n".join(lines), ha="left", va="top", fontsize=8.5, color=MUTED, linespacing=1.4
        )
        y += 0.155 * len(lines) + 0.05
    fig.legend(handles=handles, loc="lower center", ncols=ncols, frameon=False, fontsize=8, labelcolor=INK,
               handlelength=3.2, bbox_to_anchor=(0.5, 0.0))  # fmt: skip
    fig.tight_layout(rect=(0, foot / h, 1, 1 - head / h))
    out = []
    for ext in ("png", "svg"):
        p = path.with_suffix(f".{ext}")
        fig.savefig(p, dpi=200, facecolor=SURFACE)
        out.append(p.name)
    plt.close(fig)
    return out


def _caption(
    a: dict,
    m: dict,
    lv: str,
    patched: str,
    how: str,
    windows: bool = False,
    all_levels: bool = False,
    control: str | None = None,
    ci: str | None = None,
    n_text: str | None = None,
) -> list[tuple[str, str]]:
    """The caption rows (figure_terms.md's CAPTION FORMAT): What we did, Example, How to read, Control, Data."""
    level = "several prompt layouts (one per column)" if all_levels else level_text(m, lv)
    when = "at every layer of a window at once" if windows else "one layer at a time"
    n = {f: a["n_per_family"].get(f"{f}|{lv}") for f in m["families"]}
    if all_levels:
        n = {f: "/".join(str(a["n_per_family"].get(f"{f}|{x}")) for x in m["levels"]) for f in m["families"]}
    ns = n_text or ", ".join(f"{fam_title(f).split(' (')[0]} {v}" for f, v in n.items())
    per = " prompts per family"
    nkt = {f: a.get("nkt_per_family", {}).get(f"{f}|{lv}") for f in m["families"]}
    if not n_text and not all_levels and all(v and v[1] for v in nkt.values()):  # pointer_v4: entities and wordings
        ns = "; ".join(f"{fam_title(f).split(' (')[0]} {v[0]} prompts, {v[1]} entities, {v[2]} wordings"
                       for f, v in nkt.items() if v)  # fmt: skip
        per = ""
    if ci is None and a.get("ci", {}).get("kind") == "entity_cluster":
        ci = (("bars" if windows else "shading") + " = 95% interval from resampling the asked entities within each "
              "topic (entity-cluster bootstrap), widened to the item-level Wilson interval where that is wider.")  # fmt: skip
    topics = a["domains"] if all_levels else sorted(
        {k.split("|")[1].split(":")[1] for k in a["rates"] if f"|{lv}|" in k and "|domain:" in k}) or a["domains"]  # fmt: skip
    digit = "a digit (its drawer, cabinet or locker)" if m.get("data") == "pointer_v4" else "a locker digit"
    raw = (" Prompts are plain text ending in 'Answer:', with no chat template."
           if m.get("model", {}).get("prompt_format") == "raw" else "")  # fmt: skip
    rows = [
        ("What we did", f"The org prompt: {level}; each statement gives an entity {digit}. We copied the alt "
         f"prompt's hidden states ({patched}) into the org prompt, {when}, and read the answer.{raw}"),
        ("Example", a.get("example_lines", {}).get(lv) or a.get("example_line", "")),
        ("How to read", how),
        ("Control", control or "Grey: the same patch from a prompt asking about the same entity with the statements "
         "reshuffled, a random push of the same size, and a prompt from another topic. The first two should change "
         "nothing."),
        ("Data", f"{pins.MODEL_REPO.split('/')[-1]}; topics: {', '.join(topics)}; {ns}{per}; "
         + (ci or (("bars" if windows else "shading") + " = 95% Wilson interval over prompts."))),
    ]  # fmt: skip
    if a["superseded"]:
        rows.insert(0, ("Not a headline", a["superseded"]))
    if is_code(m):  # a program's "statements" are its dict entries
        rows = [(k, v.replace("statements", "dict entries").replace("statement", "dict entry")) for k, v in rows]
    return [(k, plain(v)) for k, v in rows if v]


def has_role(a: dict, lv: str, role: str) -> bool:
    """Whether a level's items predict this outcome (any read of it, or a share above 0)."""
    return any(f"|{lv}|" in k and k.endswith("|dissoc") and v.get(role, [0])[0] > 0 for k, v in a["rates"].items()) or (
        role in a.get("predicted", {}).get(lv, [])
    )


def has_token(a: dict, lv: str) -> bool:
    """Whether a level's items predict a token-position answer (pointer_v2's offset shift)."""
    return any(
        f"|{lv}|" in k and k.endswith("|dissoc") and v["token"][0] > 0 for k, v in a["rates"].items()
    ) or lv.endswith("-off")


def fig_by_layer(a: dict, m: dict, lv: str, path: Path, headline: bool = False) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams = m["families"]
    grps = [g for g in ("question", "final", "last") if g in m.get("groups", GROUPS)]
    fig, axes = plt.subplots(
        len(grps),
        len(fams),
        figsize=(max(4.2 * len(fams), 12.6), 2.6 * len(grps) + 1.6 + (1.6 if len(grps) < 3 else 0)),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for i, grp in enumerate(grps):
        for j, fam in enumerate(fams):
            ax = axes[i][j]
            _panel(ax, a, m, fam, "all", lv, grp)
            if i == 0:
                ax.set_title(fam_title(fam), fontsize=10, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel(f"patched: {GROUP_SHORT[grp]}\n% of original answers", fontsize=9, color=INK)
            if i == len(grps) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    title = ("Patch from the alt prompt: does the answer follow bridge alt's statement, its slot, or the alt "
             "prompt's own answer?") if headline else (
             f"Patch from the alt prompt: which answer does the org prompt give, by layer? ({level_text(m, lv)})")  # fmt: skip
    tr = m["windows"]["transit"]
    rows = _caption(
        a,
        m,
        lv,
        "rows: " + " / ".join(GROUP_TITLE[g] for g in grps),
        "Each coloured line: % of original answers that become that answer after the patch; dark line: % of original "
        f"answers kept. Grey band: layers {tr[0]}-{tr[-1]}, {band_words()}.",
    )
    hs = _handles(fams, token=has_token(a, lv), end=has_role(a, lv, "end"), back=has_role(a, lv, "back"))
    return _finish(fig, path, title, rows, hs, ncols=2)


def fig_slots(a: dict, m: dict, lv: str, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, slots = m["families"], ("first", "middle", "last")
    fig, axes = plt.subplots(
        len(fams), 3, figsize=(12.6, 2.6 * len(fams) + 1.6), sharex=True, sharey=True, squeeze=False
    )
    for i, fam in enumerate(fams):
        for j, slot in enumerate(slots):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, f"slot:{slot}", lv, grp, controls=("same",))
            ok = n >= MIN_N_RULE
            ax.set_title(f"{plain(fam)} · {slot} (n={n}{'' if ok else ', too few'})",
                         fontsize=9, color=INK, loc="left")  # fmt: skip
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    rows = _caption(a, m, lv, GROUP_TITLE[grp], "Columns: bridge org's statement is the first, a middle or the last "
                    f"one in the org prompt. Lines as in the main figure. Panels with fewer than {MIN_N_RULE} prompts "
                    "cannot pass the pre-registered rule.", control="Grey dashed: the same patch from a prompt about "
                    "the same entity with the statements reshuffled; it should change nothing.")  # fmt: skip
    return _finish(fig, path, "Does it matter where bridge org's statement sits (first, middle, last)?",
                   rows, _handles(fams, ("same",)), ncols=2)  # fmt: skip


def fig_domains(a: dict, m: dict, lv: str, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, doms = m["families"], a["domains"]
    fig, axes = plt.subplots(
        len(fams),
        len(doms),
        figsize=(max(4.2 * len(doms), 12.6), 2.6 * len(fams) + 1.6),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for i, fam in enumerate(fams):
        for j, dom in enumerate(doms):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, f"domain:{dom}", lv, grp)
            k = (a["rates"].get(f"{fam}|domain:{dom}|{lv}|{grp}|{sorted(m['layers'])[0]}|dissoc") or {}).get(
                "k_entities"
            )
            ax.set_title(f"{plain(fam)} · {dom} (n={n}{f', {k} entities' if k else ''})", fontsize=9, color=INK,
                         loc="left")  # fmt: skip
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    rows = _caption(
        a,
        m,
        lv,
        GROUP_TITLE[grp],
        f"One column per topic; lines as in the main figure. Grey band: {band_words()}.",
    )
    return _finish(fig, path, "Is the pattern the same for each topic?", rows, _handles(fams), ncols=2)


LEVELS_TEXT = {  # (title, how to read) of the levels figure, per dataset
    "pointer_v1": ("Does the split change with 3 statements, or with filler between the statements?",
                   "One column per prompt layout (3 statements; 5; 5 with filler sentences between them)."),
    "pointer_v2": ("Does the split change when the filler moves, or when the alt answer is also in the org prompt?",
                   "One column per alt prompt: the filler sentence moved (statement order and token position point at "
                   "different statements); the filler in place; the alt answer also in the org prompt."),
    "alias_pointer_v1": ("Does the split change when the statements name the entity in another language or by its "
                         "chemical symbol?",
                         "One column per topic and statement form, on the same scenes within a topic (animals: English "
                         "or French/Spanish/German; elements: English or the chemical symbol)."),
    "code_pointer_v1": ("Does the split change with the number of dict entries?", "One column per number of entries."),
    "pointer_v4x": ("Order, from the start, from the end, or the same place in the text: which statement does the pointer "
                    "name?",
                    "One column per alt prompt: the filler sentence moved (order vs token position), one statement more, "
                    "one fewer (the slot from the start, from the end and the token position name three different org "
                    "statements)."),
    "pointer_v5": ("Does the statement address survive word answers and longer lists?",
                   "One column per prompt layout: 5 or 8 statements, with digit or colour-word answers (the same "
                   "scenes for digits and words)."),
    "pointer_v6": ("Is the address the Nth statement, a place in the text, or a distance back from the question?",
                   "One column per alt prompt: nothing moves; an extra sentence before the list in one prompt only "
                   "(every statement moves in the text, its distance back from the question stays); an extra sentence "
                   "between the list and the question in one prompt only (the distance back changes, the place in the "
                   "text stays); long statements in both prompts."),
    "pointer_v3": ("Is the statement slot counted from the start or from the end of the list?",
                   "One column per alt prompt: one statement more, or one fewer, than the org prompt, so the slot counted "
                   "from the start and the slot counted from the end name different org statements."),
}  # fmt: skip


def level_short(m: dict, lv: str) -> str:
    """A short column name for a level."""
    data = m.get("data", "pointer_v1")
    if data == "alias_pointer_v1":
        return {"": "English", "xlang": "other language", "syn": "chemical symbol"}[lv.partition("-")[2]]
    if data == "pointer_v2":
        return {"off": "filler moved", "pln": "filler in place", "ref": "alt answer in org"}[lv.partition("-")[2]]
    if data in ("pointer_v3", "pointer_v4x"):
        return {"e5more": "alt has one statement more", "e5fewer": "alt has one statement fewer",
                "e5-off": "filler moved"}.get(lv, lv)  # fmt: skip
    if data == "pointer_v5":
        n, kind = lv[1:].split("-")
        return f"{n} statements, {'digits' if kind == 'digit' else 'colour words'}"
    if data == "pointer_v6":
        return {"e5-still": "nothing moves", "e5-abs": "extra sentence before the list",
                "e5-rel": "extra sentence before the question", "e5-long": "long statements"}.get(lv, lv)  # fmt: skip
    return {"e3f0": "3 statements", "e5f0": "5 statements", "e5f4": "5 + filler", "e8f0": "8 entries"}.get(lv, lv)


def fig_levels(a: dict, m: dict, grp: str, path: Path) -> list[str]:
    import matplotlib.pyplot as plt

    from bridge_jspace.plotting import INK

    fams, lvs = m["families"], m["levels"]
    data = m.get("data", "pointer_v1")
    if data == "alias_pointer_v1":  # each statement form exists in one topic: compare it with English in that topic
        cols = [(f"domain:{d}", lv) for d in a["domains"] for lv in lvs
                if any(k.startswith(f"{fams[0]}|domain:{d}|{lv}|") for k in a["rates"])]  # fmt: skip
    else:
        cols = [("all", lv) for lv in lvs]
    fig, axes = plt.subplots(len(fams), len(cols), figsize=(max(4.2 * len(cols), 12.6), 2.6 * len(fams) + 1.6),
                             sharex=True, sharey=True, squeeze=False)  # fmt: skip
    col_n: dict[str, list[str]] = {}
    for i, fam in enumerate(fams):
        for j, (cut, lv) in enumerate(cols):
            ax = axes[i][j]
            n = _panel(ax, a, m, fam, cut, lv, grp)
            topic = f"{cut.split(':')[1]}, " if cut != "all" else ""
            few = "" if n >= MIN_N_RULE else ", too few"
            ax.set_title(f"{fam_title(fam).split(' (')[0]} · {topic}{level_short(m, lv)} (n={n}{few})",
                         fontsize=9 if len(cols) <= 3 else 8, color=INK, loc="left")  # fmt: skip
            col_n.setdefault(fam, []).append(str(n))
            if j == 0:
                ax.set_ylabel("% of original answers", fontsize=9, color=INK)
            if i == len(fams) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    title, how = LEVELS_TEXT.get(data, LEVELS_TEXT["pointer_v1"])
    rows = _caption(a, m, lvs[0], GROUP_TITLE[grp], f"{how} Lines as in the main figure; panels with fewer than "
                    f"{MIN_N_RULE} prompts cannot pass the pre-registered rule.", all_levels=True,
                    n_text=", ".join(f"{fam_title(f).split(' (')[0]} {'/'.join(v)}" for f, v in col_n.items()))  # fmt: skip
    return _finish(fig, path, title, rows, _handles(fams, token=any(has_token(a, lv) for lv in lvs),
                                                   end=any(has_role(a, lv, "end") for lv in lvs),
                                                   back=any(has_role(a, lv, "back") for lv in lvs)), ncols=2)  # fmt: skip


def fig_windows(a: dict, m: dict, lv: str, path: Path) -> list[str]:
    """The window patches (every layer of the window at once): each outcome's share with its Wilson interval, next to
    the 'same' control's change rate."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, percent_axis, style_axes

    fams, wins = m["families"], list(m["windows"])
    grps = [g for g in GROUPS if g in m.get("groups", GROUPS)]
    roles = ("none", "identity", "position", *(("end",) if has_role(a, lv, "end") else ()),
             *(("token",) if has_token(a, lv) else ()), *(("back",) if has_role(a, lv, "back") else ()),
             "value")  # fmt: skip
    col = {"none": NONE_COLOR, **OUTCOME_COLOR}
    fig, axes = plt.subplots(
        len(grps),
        len(fams),
        figsize=(max(4.2 * len(fams), 12.6), 2.3 * len(grps) + 1.6),
        sharex=True,
        sharey=True,
        squeeze=False,
    )
    for i, grp in enumerate(grps):
        for j, fam in enumerate(fams):
            ax = axes[i][j]
            style_axes(ax)
            for wi, w in enumerate(wins):
                d = a["rates"].get(f"{fam}|all|{lv}|{grp}|{w}|dissoc")
                s = a["rates"].get(f"{fam}|all|{lv}|{grp}|{w}|same")
                if not d:
                    continue
                for ri, role in enumerate(roles):
                    if fam == family_roles(m)[2] and role == "value":
                        continue
                    x = wi + (ri - (len(roles) - 1) / 2) * 0.15
                    r, lo, hi = d[role]
                    ax.errorbar([x], [r], yerr=[[r - max(lo, 0)], [hi - r]], fmt="o", ms=5, color=col[role], ecolor=col[role], elinewidth=1.4, capsize=0)  # fmt: skip
                if s:
                    r, lo, hi = s["changed"]
                    ax.errorbar([wi + 0.42], [r], yerr=[[r - max(lo, 0)], [hi - r]], fmt="s", ms=4, mfc="none",
                                color=CONTROL_STYLE["same"][0], elinewidth=1, capsize=0)  # fmt: skip
            ax.set_xticks(
                range(len(wins)), [f"{w}\n{m['windows'][w][0]}-{m['windows'][w][-1]}" for w in wins], fontsize=8
            )
            ax.set_ylim(-0.02, 1.05)
            percent_axis(ax)
            if i == 0:
                ax.set_title(fam_title(fam), fontsize=10, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel(f"patched: {GROUP_SHORT[grp]}\n% of original answers", fontsize=9, color=INK)
    handles = [Line2D([], [], color=col[r], marker="o", ls="none", ms=5,
                      label="% of original answers kept" if r == "none" else f"% that become {OUTCOME_TERM[r].removeprefix('the ')}")
               for r in roles]  # fmt: skip
    handles.append(Line2D([], [], color=CONTROL_STYLE["same"][0], marker="s", mfc="none", ls="none", ms=4,
                          label=CONTROL_LABEL["same"]))  # fmt: skip
    rows = _caption(a, m, lv, "rows: " + " / ".join(GROUP_TITLE[g] for g in grps),
                    "Each dot: % of original answers that become that answer when a whole window of layers is patched; "
                    "the pre-registered main test is memory → prompt, everything after the question, layers 44-52.",
                    windows=True, control="Grey squares: the same patch from a prompt about the same entity with the "
                    "statements reshuffled (% changed); it should change nothing.")  # fmt: skip
    return _finish(fig, path, "Patching a whole window of layers from the alt prompt: which answer wins?", rows,
                   handles, ncols=3)  # fmt: skip


PRIMARY_RUNS = ("d3_main_ae_27b", "d3_levels_animals_27b")
LEDGER = pins.RESULTS_DIR / "jobq" / "ledger.jsonl"


def _commit(name: str) -> str:
    if LEDGER.exists():
        for line in LEDGER.read_text().splitlines():
            r = json.loads(line)
            if r.get("id") == name and r.get("commit"):
                return r["commit"][:7]
    return "unknown"


def _pct(x: list[float] | None) -> str:
    return f"{100 * x[0]:.0f}% [{100 * x[1]:.0f}, {100 * x[2]:.0f}]" if x else "-"


def _shares(d: dict | None, roles=("none", "identity", "position", "value")) -> str:
    return ", ".join(f"{OUTCOME_TERM[r]} {_pct(d[r])}" for r in roles) if d else "-"


COMPETENCE_RUN = "d3_competence_27b"


def dan_section(a: dict) -> list[str]:
    """Dan's written D3 predictions (predictions/2026-10-20_dan.md) next to this run's numbers. The numbers are
    computed; the last column is the agent's reading of them."""
    r, s = a["rates"], a["strongest_layer"]

    def sh(d: dict) -> str:
        return " / ".join(f"{100 * d[x][0]:.0f}" for x in ("identity", "position", "value", "none"))

    comp = PV.RESULTS / COMPETENCE_RUN / "summary.json"
    q31 = "-"
    if comp.exists():
        c = json.loads(comp.read_text())["labels"]
        q31 = "; ".join(f"{d} {_pct([c[f'main/{d}_RL_e5f0']['cells']['clean'][k] for k in ('rate', 'lo', 'hi')])}"
                        for d in PV.DOMAINS if f"main/{d}_RL_e5f0" in c)  # fmt: skip
    rq, rl = s["RL|e5f0|question"], s["RL|e5f0|last"]
    rl50 = r["RL|all|e5f0|last|50|dissoc"]
    slots = "; ".join(
        f"{sl} n={r[f'RL|slot:{sl}|e5f0|final|transit|dissoc']['n']} {OUTCOME_TERM['position']} "
        f"{_pct(r[f'RL|slot:{sl}|e5f0|final|transit|dissoc']['position'])}"
        for sl in ("first", "middle", "last")
    )
    rr, dq = s["RR|e5f0|question"], s["DL|e5f0|question"]
    rr_last = r["RR|all|e5f0|last|transit|dissoc"]
    dl_q = max((r[f"DL|all|e5f0|question|{la}|dissoc"]["position"][0], la) for la in range(16, 46, 2))
    dl_f50 = r["DL|all|e5f0|final|50|dissoc"]
    prim = r["RL|all|e5f0|final|transit|dissoc"]
    q_tr = r["RL|all|e5f0|question|transit|dissoc"]
    T = OUTCOME_TERM
    rows = [
        ("Q3.1 memory → prompt with 5 statements >= 80%?", "yes, >= 95%",
         f"org prompt answered (main, first 100 per topic): {q31}",
         "partly: >= 80% for 3 of 4 topics; >= 95% only for animals; months fail"),
        ("Q3.2 memory → prompt, patch the question words: shares at the strongest layer", "60 / 10 / 10 / 20",
         f"layer {rq['layer']}: {sh(rq)}", f"direction right ({T['identity']}), more extreme; from layer 40 on the "
         f"question words carry nothing (layers 44-52: {T['none']} {100 * q_tr['none'][0]:.0f}%)"),
        ("Q3.3 memory → prompt, patch only the last tokens", "80 / 10 / 5 / 5",
         f"strongest layer {rl['layer']}: {sh(rl)}; at layer 50: {sh(rl50)}",
         f"wrong: the last tokens give the {T['position']} (layer 50), then {T['value']} (52+); "
         f"{T['identity']} never above ~25%"),
        ("Q3.4 does it depend on where bridge org's statement sits?", "no",
         f"memory → prompt, everything after the question, layers 44-52: {slots}",
         "undetermined: first/last panels have n < 35 (the rule cannot pass); first is lowest, not highest as Mixing "
         "Mechanisms predicts"),
        ("Q3.5 memory → memory (a pointer is useless)", "85 / 5 / 5 / 5",
         f"question words, layer {rr['layer']}: {sh(rr)}; last two tokens, layers 44-52: {T['identity']} "
         f"{_pct(rr_last['identity'])}, {T['position']} {_pct(rr_last['position'])}",
         f"right: {T['identity']} (here the same digit as {T['value']}); {T['position']} ~0 everywhere"),
        ("Q3.5 named → prompt (direct question)", "80 / 5 / 5 / 10",
         f"question words, layer {dq['layer']}: {sh(dq)}; question words, layer {dl_q[1]}: {T['position']} "
         f"{100 * dl_q[0]:.0f}%; everything after the question, layer 50: {sh(dl_f50)}",
         f"partly wrong: from layer 28 the question words give the {T['position']} for ~40% of prompts, and the "
         f"tokens after the question give it before {T['value']}"),
        ("Q3.6 what the lens reads but cannot steer", "the word dominates; the statement's slot has little effect",
         f"memory → prompt, everything after the question, layers 44-52: {sh(prim)}",
         "contradicted at 44-52: the bridge is no longer on the question words; the tokens after the question carry "
         f"a pointer to the statement's slot ({T['position']}, more than {T['identity']}), then the answer itself; "
         "pooled verdict 'same statement slot', but 'mixed' for each topic alone"),
    ]  # fmt: skip
    out = ["", "## Dan's predictions (predictions/2026-10-20_dan.md, D3) vs results", "",
           f"Shares are {T['identity']} / {T['position']} / {T['value']} / {T['none']}, in % of prompts.", "",
           "| question | Dan | result (this run unless said) | reading |", "|---|---|---|---|"]  # fmt: skip
    out += [f"| {q} | {d} | {res} | {rd} |" for q, d, res, rd in rows]
    return out


def prior_checks(m: dict, a: dict) -> list[str]:
    """Each job-spec hypothesis's numeric prediction against the run (main-type and levels-type runs)."""
    pf, rf, cf = family_roles(m)
    r = a["rates"]
    lvs = m["levels"]
    lv = "e5f0" if "e5f0" in lvs else lvs[0]
    T = OUTCOME_TERM

    def c(fam: str, grp: str, w: str = "transit", level: str = lv) -> dict:
        return r.get(f"{fam}|all|{level}|{grp}|{w}|dissoc") or {x: [float("nan")] * 3 for x in (*ROLES, "changed")}

    def onset(grp: str) -> int | None:
        return next((la for la in sorted(m["layers"]) if c(pf, grp, str(la))["value"][0] >= 0.2), None)

    def yn(ok: bool) -> str:
        return "met" if ok else "not met"

    if a["level_contrasts"]:
        out = []
        for k, cc in a["level_contrasts"].items():
            d = cc["diffs"]
            out.append(f"- {k} (interpretable: {cc['interpretable']}): " + ", ".join(
                f"{T[x]} {100 * d[x]['diff'][0]:+.0f} [{100 * d[x]['diff'][1]:+.0f}, {100 * d[x]['diff'][2]:+.0f}] "
                f"{d[x]['label']}" for x in PV.HYPOTHESES))  # fmt: skip
        win = max(("identity", "position", "value"), key=lambda x: c(pf, "final")[x][0])
        out.append(f"- H-robust / H-contiguity: this run's leading outcome at 5 statements (memory → prompt, everything "
                   f"after the question, layers 44-52) is '{T[win]}'; e5f4 vs e5f0 for it: see the rows above "
                   f"('same' = within 0.15 supports H-robust, 'differs' with a drop H-contiguity, 'unclear' neither).")  # fmt: skip
        out.append(f"- H-fewer-entities: the e3f0_vs_e5f0 '{T['position']}' entries above ('differs' with a positive "
                   "difference supports it).")  # fmt: skip
        return out
    f_, l_ = c(pf, "final"), c(pf, "last")
    rr_f, rr_l, dl_f = c(cf, "final"), c(cf, "last"), c(rf, "final")
    return [
        f"- H-pointer: memory → prompt, {T['position']}: after the question {_pct(f_['position'])}, last two tokens "
        f"{_pct(l_['position'])} (>= 50%: {yn(f_['position'][0] >= 0.5 or l_['position'][0] >= 0.5)}); memory → "
        f"memory {_pct(rr_f['position'])} / {_pct(rr_l['position'])} (<= 10%: "
        f"{yn(max(rr_f['position'][0], rr_l['position'][0]) <= 0.1)}); named → prompt after the question "
        f"{_pct(dl_f['position'])} (>= 50%: {yn(dl_f['position'][0] >= 0.5)})",
        f"- H-word: memory → prompt, {T['identity']}: {_pct(f_['identity'])} / {_pct(l_['identity'])} (>= 50%: "
        f"{yn(max(f_['identity'][0], l_['identity'][0]) >= 0.5)})",
        f"- H-value: memory → prompt, {T['value']}: {_pct(f_['value'])} / {_pct(l_['value'])} (>= 50%: "
        f"{yn(max(f_['value'][0], l_['value'][0]) >= 0.5)}); first single layer where it reaches 20%: after the "
        f"question {onset('final')}, last two tokens {onset('last')}",
        f"- H-none: memory → prompt, answer changed after the question {_pct(f_['changed'])} (< 20%: "
        f"{yn(f_['changed'][0] < 0.2)})",
    ]


def report_md(name: str, m: dict, a: dict, out: Path) -> str:
    """AGENTS.md's report block, the rule's verdicts (with cuts and reachability), checks, Dan's predictions, priors."""
    pf = family_roles(m)[0]
    r, v = a["rates"], a["verdicts"]
    lvs = m["levels"]
    main_lv = "e5f0" if "e5f0" in lvs else lvs[0]
    n_fam = {k: x for k, x in a["n_per_family"].items()}
    prim = r.get(f"{pf}|all|{main_lv}|final|transit|dissoc")
    same = r.get(f"{pf}|all|{main_lv}|final|transit|same")
    tr = m["windows"]["transit"]
    rand_l = [r.get(f"{pf}|all|{main_lv}|final|{la}|rand") for la in tr]
    rand_changed = max((x["changed"] for x in rand_l if x), default=None, key=lambda t: t[0])
    other_l = [r.get(f"{pf}|all|{main_lv}|final|{la}|other") for la in tr]
    other_changed = max((x["changed"] for x in other_l if x), default=None, key=lambda t: t[0])
    where = out.relative_to(pins.REPO_ROOT) if out.is_relative_to(pins.REPO_ROOT) else out
    figs = [f"{where}/{f}" for fs in a["figures"].values() for f in fs if f.endswith(".png")]
    import yaml

    titles = pins.REPO_ROOT / "jobs" / "titles.yaml"
    spec_file = pins.REPO_ROOT / "jobs" / "d3" / f"{name}.yaml"
    title = name
    if spec_file.exists():  # a job spec's own title, else jobs/titles.yaml (older runs)
        title = (yaml.safe_load(spec_file.read_text()) or {}).get("title", name)
    if title == name and titles.exists():
        title = (yaml.safe_load(titles.read_text()) or {}).get(name, name)
    lines = [
        f"# {title}",
        "",
        f"Run `{name}` (results/pointer_swap/), analysis of the saved outputs only.",
        "",
        "Level names: " + "; ".join(f"`{lv}` = {level_text(m, lv)}" for lv in lvs) + ".",
        "",
    ]
    if a["superseded"]:
        lines += [f"**NOT A HEADLINE RUN (superseded or smoke)**: {a['superseded']}. Shown for completeness.", ""]
    seeds = json.dumps(list(m.get("seeds", {"sample": 0}).values()))
    nkt = a.get("nkt_per_family", {})

    def n_of(k: str, v: int) -> str:
        x = nkt.get(k)
        return f"{v} items / {x[1]} entities / {x[2]} wordings" if x and x[1] else str(v)

    if a.get("ci", {}).get("kind") == "entity_cluster":
        lines += ["Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, "
                  "seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. "
                  "Item-level Wilson: summary.json `rates[...]['wilson']`.", ""]  # fmt: skip
    lines += [
        "```",
        f"EXP {name} @ {_commit(name)} | model {m['model']['repo'].split('/')[-1]} "
        f"({m['model'].get('prompt_format', 'chat')} format) | n per family = "
        + "; ".join(
            f"{fam_title(k.split('|')[0]).split(' (')[0]} {n_of(k, v)} ({level_short(m, k.split('|')[1])})"
            for k, v in n_fam.items()
        )
        + f" | seeds={seeds} (sample, null, other)",
        "Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers "
        f"{tr[0]}-{tr[-1]}: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the "
        "answer (H-value)",
        f"Headline: RL, tokens after the question, transit window ({main_lv}): position = {_pct(prim['position']) if prim else '-'}   "
        f"Baseline: none = {_pct(prim['none']) if prim else '-'}, identity = {_pct(prim['identity']) if prim else '-'}, "
        f"value = {_pct(prim['value']) if prim else '-'}   Control: 'same' changed = {_pct(same['changed']) if same else '-'}; "
        f"random direction changed (max over transit layers) = {_pct(rand_changed)}; other item changed = {_pct(other_changed)}",
        f"Figures: {', '.join(figs)}",
        "Three dumbest ways this could be wrong: see below",
        f"For the human to verify: results/pointer_swap/{name}/outcomes.jsonl, rows `family == 'RL'`, "
        f"`group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == '{main_lv}'`: count `role` "
        f"(n={prim['n'] if prim else '-'}); position should be "
        f"{prim['k'].get('position', 0) if prim else '-'}, identity {prim['k'].get('identity', 0) if prim else '-'}, value "
        f"{prim['k'].get('value', 0) if prim else '-'}, none {prim['k'].get('none', 0) if prim else '-'}",
        "Status: UNVERIFIED",
        "```",
        "",
    ]
    ch = a["checks"]
    nt = a["near_ties"]
    dom_v = {dm: v.get(f"{pf}|domain:{dm}|{main_lv}|final|transit", {}).get("verdict") for dm in a["domains"]}
    dumb = [
        "Position here could be the absolute token offset rather than the statement's order: statements have equal "
        "length, so the two coincide (the filler level keeps the same layout in base and source and does not separate "
        "them). Not checked; needs an offset-shift variant.",
        f"Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. "
        f"Checked: the random-direction control at the same per-token norm changes RL's answer {_pct(rand_changed)} "
        f"(max over transit layers); digits of the base context that no hypothesis predicts win "
        f"{_pct(prim['context']) if prim else '-'}; among dissoc reads won by a predicted digit, "
        f"{nt['within_gap']}/{nt['n']} have the runner-up prediction within p {nt['gap']}; hook checks "
        f"self no-op {ch['self_noop']['same_top']}/{ch['self_noop']['n']}, layer-0 reproduction "
        f"{ch['layer0_all_reproduces_source']['same_top']}/{ch['layer0_all_reproduces_source']['n']}.",
        f"The pooled verdict could rest on pooling: per domain the same cell's verdict is {json.dumps(dom_v)}; the "
        f"spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.",
    ]
    lines += ["## Three dumbest ways this could be wrong", ""] + [f"{i + 1}. {t}" for i, t in enumerate(dumb)] + [""]
    lines += [
        "## Pre-registered decision rule and its verdict",
        "",
        "Rule (scripts/pointer_swap.py docstring, written before any run):",
        "",
        "> " + rule_plain(m["decision"].replace("\n", " ")),
        "",
        "Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): "
        + "; ".join(
            f"{lv}: **{VERDICT_TERM.get(a['primary'][lv]['verdict'].get('verdict', 'no data'))}** "
            f"({_shares(a['primary'][lv]['rates'])})"
            for lv in lvs
        ),
        "",
        f"A cell needs n >= {MIN_N_RULE} items for the 'same' control's Wilson upper bound to reach <= {DAMAGE_MAX} even "
        f"with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives "
        f"'damage'. Cells where the rule cannot pass: {a['rule_unreachable_cells']['count']}, in cuts "
        f"{a['rule_unreachable_cells']['cuts']}.",
        "",
        "| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |",
        "|---|---|---|---|---|---|",
    ]
    for fam in m["families"]:
        for grp in GROUPS:
            for lv in lvs:
                cells = []
                for w in m["windows"]:
                    vv = v.get(f"{fam}|all|{lv}|{grp}|{w}", {})
                    d = r.get(f"{fam}|all|{lv}|{grp}|{w}|dissoc")
                    top = max(("identity", "position", "value"), key=lambda x: d[x][0]) if d else None
                    cells.append(
                        f"{VERDICT_TERM.get(vv.get('verdict', '-'), '-')} (answer org kept {100 * d['none'][0]:.0f}%, "
                        f"{OUTCOME_TERM[top]} {100 * d[top][0]:.0f}%)"
                        if d and top
                        else "-"
                    )
                lines.append(f"| {fam} | {GROUP_TITLE[grp]} | {lv} | " + " | ".join(cells) + " |")
    lines += ["", "Cuts of the primary cell (RL, tokens after the question, transit window):", "",
              "| cut | level | n | same n | verdict | rule reachable | shares |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for lv in lvs:
        for cut in ["all", *(f"domain:{d}" for d in a["domains"]), "slot:first", "slot:middle", "slot:last"]:
            vv = v.get(f"{pf}|{cut}|{lv}|final|transit")
            if not vv:
                continue
            d = r.get(f"{pf}|{cut}|{lv}|final|transit|dissoc")
            sm = r.get(f"{pf}|{cut}|{lv}|final|transit|same")
            dmg = f" ({sm['n'] - sm['k'].get('none', 0)} 'same' changes)" if vv["verdict"] == "damage" and sm else ""
            lines.append(f"| {cut} | {lv} | {vv['n']} | {vv['n_same']} | {VERDICT_TERM[vv['verdict']]}{dmg} | "
                         f"{'yes' if vv['rule_reachable'] else 'NO (n < 35)'} | {_shares(d)} |")  # fmt: skip
    lines += ["", "## Checks", "", f"`{json.dumps(a['checks'])}`; near ties: `{json.dumps(a['near_ties'])}`", ""]
    lines += ["## Strongest single layer per family and patch site (largest share changed; earliest on ties)", "",
              f"| family | level | patched tokens | layer | changed | {OUTCOME_TERM["none"]} | {OUTCOME_TERM["identity"]} | {OUTCOME_TERM["position"]} | {OUTCOME_TERM["value"]} |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for k, s in a["strongest_layer"].items():
        fam, lv, grp = k.split("|")
        lines.append(f"| {fam} | {lv} | {GROUP_TITLE[grp]} | {s['layer']} | {_pct(s['changed'])} | {_pct(s['none'])} | "
                     f"{_pct(s['identity'])} | {_pct(s['position'])} | {_pct(s['value'])} |")  # fmt: skip
    if a["level_contrasts"]:
        lines += ["", "## Level contrasts (spec rule: Newcombe 95% interval of the share difference vs e5f0; 'same' "
                  "if within +-0.15, 'differs' if it excludes 0 and |diff| > 0.15)", "",
                  f"| contrast | interpretable | {OUTCOME_TERM["none"]} | {OUTCOME_TERM["identity"]} | {OUTCOME_TERM["position"]} | {OUTCOME_TERM["value"]} |", "|---|---|---|---|---|---|"]  # fmt: skip
        for k, c in a["level_contrasts"].items():
            cells = [f"{100 * c['diffs'][x]['diff'][0]:+.0f} [{100 * c['diffs'][x]['diff'][1]:+.0f}, "
                     f"{100 * c['diffs'][x]['diff'][2]:+.0f}] {c['diffs'][x]['label']}" for x in PV.HYPOTHESES]  # fmt: skip
            lines.append(f"| {k} | {c['interpretable']} | " + " | ".join(cells) + " |")
    if a.get("ref_contrasts"):
        lines += ["", "## Reflexive test (pre-registered v2 rule): the alt prompt's own answer, when it is also in the org "
                  "prompt vs when it is not (same scenes, paired)", "",
                  "| family | patched tokens | layer | pairs | alt answer, also in org | alt answer, not in org | "
                  "difference [95% CI] | label | plain cell interpretable |", "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for k, c in a["ref_contrasts"].items():
            fam, _lv, grp, layer = k.split("|")
            if fam != pf or grp not in ("final", "last"):
                continue
            dd = c["diff"]
            lines.append(f"| {fam} | {GROUP_TITLE[grp]} | {layer} | {c['n_pairs']} | {100 * c['ref_value']:.0f}% | "
                         f"{100 * c['pln_value']:.0f}% | {100 * dd[0]:+.0f} [{100 * dd[1]:+.0f}, {100 * dd[2]:+.0f}] | "
                         f"{c['label']} | {c['interpretable']} |")  # fmt: skip
    if a.get("v4x"):
        x = a["v4x"]
        T = OUTCOME_TERM
        lines += ["", "## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers "
                  f"{' and '.join(primary_layers(m))}", "",
                  f"H-order-v4 (filler moved: {T['position']} beats {T['token']}, pooled and in >= 2 of 3 topics at one "
                  f"layer): **{'holds' if x['H-order-v4']['holds'] else 'does not hold'}**; H-start-v4 (one more / one "
                  f"fewer: the slot from the start beats {T['end']} and {T['token']}, pooled and in >= 2 topics, both alt "
                  f"types, one layer): **{'holds' if x['H-start-v4']['holds'] else 'does not hold'}**.", "",
                  "| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' "
                  "upper bounds |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for key, c in x["cells"].items():
            lv, la, cut = key.split("|")
            rivals = "; ".join(f"{r} {_pct(c[r])}" for r in V4X_TESTS[lv][1])
            lines.append(f"| {level_short(m, lv)} | {la} | {cut} | {c['n']} | {c['k_entities']} | {_pct(c['winner'])} | "
                         f"{rivals} | {'yes' if c['beats'] else 'no'}{'' if c['reachable'] else ' (n < 35)'} |")  # fmt: skip
    if a.get("v5"):
        lines += ["", "## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers "
                  f"{' and '.join(primary_layers(m))}: does each layout keep the statement slot?", "",
                  "| layout | keeps the slot | per layer: pooled verdict, topics with the slot |", "|---|---|---|"]  # fmt: skip
        for lv, c in a["v5"].items():
            per = "; ".join(f"{la}: {v['pooled']}, {len(v['topics_with_slot'])}/3" for la, v in c["layers"].items())
            lines.append(f"| {level_short(m, lv)} | **{'yes' if c['holds'] else 'no'}** | {per} |")
    if a.get("v6"):
        x = a["v6"]
        yes = {True: "holds", False: "does not hold"}
        lines += ["", "## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers "
                  f"{' and '.join(primary_layers(m))}, pooled", "",
                  f"H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the "
                  f"place in the text): **{yes[x['H-rel']]}**; H-abs (the opposite): **{yes[x['H-abs']]}**; H-ordinal "
                  f"(the same slot beats the moved statement under both shifts): **{yes[x['H-ordinal']]}**; H-long "
                  f"(Dan: long statements lower the same-slot share): **{yes[x['H-long']]}**.", "",
                  "| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | "
                  "slot: abs / rel | slot: still / long | long - still [95%] |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for la, c in x["layers"].items():
            if not c:
                continue
            lines.append(f"| {la} | {c['n'][0]} / {c['n'][1]} | {_pct(c['moved_abs'])} | {_pct(c['moved_rel'])} | "
                         f"{_pct(c['rel_minus_abs'])} | {_pct(c['slot_abs'])} / {_pct(c['slot_rel'])} | "
                         f"{_pct(c.get('slot_still'))} / {_pct(c.get('slot_long'))} | {_pct(c.get('long_minus_still'))} |")  # fmt: skip
    if name == "d3_main_ae_27b":
        lines += dan_section(a)
    lines += ["", "## Agent priors in the job spec (jobs/d3/" + name + ".yaml `hypotheses`) vs results", ""]
    spec = pins.REPO_ROOT / "jobs" / "d3" / f"{name}.yaml"
    if spec.exists():
        import yaml

        for h, txt in yaml.safe_load(spec.read_text())["hypotheses"].items():
            lines.append(f"- {h}: {rule_plain(txt)}")
    lines += ["", "Against the saved numbers:", "", *prior_checks(m, a), ""]
    ex = RESULTS / name / "examples.json"
    if ex.exists():
        e = json.loads(ex.read_text())
        pick = (
            next((x for x in e["examples"] if x["group"] == "position" and x["family"] == pf), None)
            or (e["examples"] or [None])[0]
        )
        if pick:
            exp, pp = pick["answers"]["expected"], pick["numbers"]["p"]
            outcome = OUTCOME_TERM.get(pick["group"], pick["group"])
            lines += ["## Worked example (from examples.json)", "", f"Item `{pick['item_id']}` ({pick['family']}; the "
                      f"patched answer was the {outcome}). {pick['condition']}.", "", "Org prompt (as fed):", "", "```",
                      pick["prompt"], "```", "", "Alt prompt:", "", "```", pick["source_prompt"], "```", "",
                      f"Answers: answer org {pick['answers']['clean']}; after the patch {pick['answers']['edited']}. "
                      "Predicted: " + "; ".join(f"{OUTCOME_TERM[h]} {exp[h]} (p {pp.get(h, 0):.3f})" for h in HYPS
                                         if exp.get(h, "-") != "-")
                      + ".", ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def fig_ref(a: dict, m: dict, path: Path) -> list[str]:
    """pointer_v2's reflexive test: the alt prompt's own answer by layer, when it is also in the org prompt (ref) and
    when it is not (pln), on the same scenes; the paired difference's 95% CI shaded."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, percent_axis, style_axes

    pf, rf, _ = family_roles(m)
    fams = [f for f in (pf, rf) if f in m["families"]]
    grps = ("final", "last")
    refs = [lv for lv in m["levels"] if lv.endswith("-ref")]
    fig, axes = plt.subplots(len(grps), len(fams) * len(refs), figsize=(max(4.4 * len(fams) * len(refs), 12.6), 7.4), sharex=True,
                             sharey=True, squeeze=False)  # fmt: skip
    layers = sorted(m["layers"])
    for j, (fam, ref) in enumerate([(f, r) for r in refs for f in fams]):
        for i, grp in enumerate(grps):
            ax = axes[i][j]
            style_axes(ax)
            tr = m["windows"]["transit"]
            _band(ax, tr[0], tr[-1], None)
            xs, rr, rp, lo, hi = [], [], [], [], []
            for la in layers:
                c = a["ref_contrasts"].get(f"{fam}|{ref}|{grp}|{la}")
                if c:
                    xs.append(la)
                    rr.append(c["ref_value"])
                    rp.append(c["pln_value"])
                    lo.append(c["pln_value"] + c["diff"][1])
                    hi.append(c["pln_value"] + c["diff"][2])
            ax.fill_between(xs, lo, hi, color=OUTCOME_COLOR["value"], alpha=0.14, lw=0)
            ax.plot(xs, rr, color=OUTCOME_COLOR["value"], lw=2)
            ax.plot(xs, rp, color=OUTCOME_COLOR["value"], lw=1.4, ls=(0, (4, 2)))
            ax.set_ylim(-0.02, 1.05)
            percent_axis(ax)
            if i == 0:
                ax.set_title(f"{fam_title(fam).split(' (')[0]} · {level_text(m, ref).split(',')[0]}", fontsize=9,
                             color=INK, loc="left")  # fmt: skip
            if j == 0:
                ax.set_ylabel(f"patched: {GROUP_SHORT[grp]}\n% of original answers", fontsize=9, color=INK)
            if i == len(grps) - 1:
                ax.set_xlabel("layer patched", fontsize=9, color=INK)
    handles: list[Any] = [
        Line2D([], [], color=OUTCOME_COLOR["value"], lw=2, label="% that become the alt prompt's answer, which the org prompt also has"),
        Line2D([], [], color=OUTCOME_COLOR["value"], lw=1.4, ls=(0, (4, 2)), label="% that become the alt prompt's answer, which the org prompt does not have"),
    ]  # fmt: skip
    rows = _caption(a, m, refs[0], "everything after the question / the last 2 tokens",
                    "Solid vs dashed: the same scenes, the alt prompt's answer present in the org prompt or not. Shading: "
                    "95% CI of the paired difference around the dashed line. A pointer to the answer token needs the "
                    "digit in the prompt (solid above dashed); a digit carried as content does not (lines together).",
                    control="Pre-registered: 'reflexive' if the difference's lower bound is above +10 points, 'content' "
                    "if its CI lies within ±10 points.", ci="shading = paired-bootstrap 95% CI of the difference.")  # fmt: skip
    return _finish(
        fig, path, "Does the alt prompt's answer need to be in the org prompt to come out?", rows, handles, ncols=1
    )


def no_cases_report(name: str, m: dict) -> str:
    """report.md of a run that patched nothing: which scenes the competence gate left, per topic and layout."""
    summ = RESULTS / name / "summary.json"
    counts = json.loads(summ.read_text()).get("counts", {}) if summ.exists() else {}
    rows = [f"| {k} | {v.get('eligible_scenes', 0)} | {v.get('sampled', 0)} |" for k, v in sorted(counts.items())]
    return "\n".join([
        f"# {name}: no eligible cases", "",
        f"Nothing was patched: no scene was answered right in every prompt of every family of the run by the "
        f"competence run `{m.get('competence')}` ({m.get('model', {}).get('prompt_format', 'chat')} format), so there "
        "are no outcomes, figures or verdicts. Look at the competence run before reading anything into this one.", "",
        "| topic / layout | eligible scenes | sampled |", "|---|---|---|", *rows, "",
    ])  # fmt: skip


def stage_figures(name: str) -> Path:
    """Re-applies the rule (analyze), draws the run's figures, writes summary.json and report.md into a new
    results/pointer_swap/<run>/analysis-<stamp>-figures/."""
    import matplotlib

    matplotlib.use("Agg")
    m, rows, checks = load_run(name)
    import shutil

    for old in (RESULTS / name).glob("analysis-*-figures"):  # one figures folder per run (the user's rule)
        shutil.rmtree(old)
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    out.mkdir()
    if not any(o["source"] == "dissoc" for o in rows):  # nothing was patched: say so instead of drawing empty figures
        (out / "report.md").write_text(no_cases_report(name, m))
        (out / "summary.json").write_text(json.dumps({"run": name, "cases": 0, "figures": {}}, indent=1) + "\n")
        print("wrote", out, "(no eligible cases)")
        return out
    a = analyze(m, rows, checks)
    a["near_ties"] = near_ties(rows)
    a["example_line"] = example_line(m, name)
    a["example_lines"] = {lv: example_line(m, name, lv) for lv in m["levels"]}
    figs: dict[str, list[str]] = {}
    main_lv = "e5f0" if "e5f0" in m["levels"] else m["levels"][0]
    for lv in m["levels"]:
        figs[f"by_layer_{lv}"] = fig_by_layer(
            a, m, lv, out / f"by_layer_{lv}", headline=(name in PRIMARY_RUNS and lv == main_lv)
        )
    figs["slots_final"] = fig_slots(a, m, main_lv, "final", out / f"slots_final_{main_lv}")
    figs["slots_last"] = fig_slots(a, m, main_lv, "last", out / f"slots_last_{main_lv}")
    figs["windows"] = fig_windows(a, m, main_lv, out / f"windows_{main_lv}")
    if len(a["domains"]) > 1:
        figs["domains_final"] = fig_domains(a, m, main_lv, "final", out / f"domains_final_{main_lv}")
    if m.get("data") == "pointer_v4x":  # the primary is the last two tokens per topic: one topics figure per layout
        for lv in m["levels"]:
            figs[f"domains_last_{lv}"] = fig_domains(a, m, lv, "last", out / f"domains_last_{lv}")
    if len(m["levels"]) > 1:
        figs["levels_final"] = fig_levels(a, m, "final", out / "levels_final")
        figs["levels_last"] = fig_levels(a, m, "last", out / "levels_last")
    if a.get("ref_contrasts"):
        figs["reflexive"] = fig_ref(a, m, out / "reflexive")
    a["figures"] = figs
    (out / "summary.json").write_text(json.dumps(a, indent=1) + "\n")
    (out / "report.md").write_text(plain(report_md(name, m, a, out)))
    print("wrote", out)
    return out


# ---- examples -------------------------------------------------------------------------------------------------------


GROUP_DEFS = {
    "position": "the patched base answered the base's digit at the source's queried slot (H-pointer's prediction)",
    "token": "the patched base answered the base's digit at the source statement's token offset (H-token)",
    "end": "the patched base answered the base's digit at the source's slot counted from the end (H-end)",
    "back": "the patched base answered the base's digit as far back from the question as the source's statement (H-rel)",
    "identity": "the patched base answered the base's digit for the source's entity (H-word / lexical key)",
    "value": "the patched base answered the source's own answer, absent from the base context (H-value)",
    "none": "the patch left the base answer",
    "context": "another digit of the base context, predicted by no hypothesis",
    "other": "any other answer (a recalled digit, another digit, a word)",
    "same_changed": "control: the 'same' source (every hypothesis predicts the base answer) changed the answer",
}


def char_spans(offsets: list[tuple[int, int]], positions: list[int]) -> list[tuple[int, int]]:
    """Merge the tokens' char spans into contiguous runs."""
    spans: list[list[int]] = []
    for i in sorted(positions):
        if i >= len(offsets):
            continue
        s, e = offsets[i]
        if spans and s <= spans[-1][1]:
            spans[-1][1] = max(spans[-1][1], e)
        else:
            spans.append([s, e])
    return [(s, e) for s, e in spans]


def statement_char_spans(text: str, item: dict, order: list[str], digits: list[int]) -> list[tuple[int, int]]:
    """Char spans of the prompt's statements (in order; pointer_v1/v2 and alias items). Code items have none: []."""
    base = order == item["entities"] and digits == item["digits"]
    ctx = item["context"] if base else item["sources"]["dissoc"]["context"]
    if "statements" in item:  # alias_pointer_v1 records every prompt's statements
        return PV.statement_spans(text, ctx, item["statements"] if base else item["sources"]["dissoc"]["statements"])
    part = item if base else item["sources"]["dissoc"]
    if "entries" in part.get("spans", {}):  # code_pointer_v1: the dict entries, offsets in the user turn's content
        at = text.index(ctx)
        return [(at + s, at + e) for s, e in part["spans"]["entries"]]
    if item["domain"] not in PV.DOMAINS:
        return []
    facts = [PV.DOMAINS[item["domain"]]["statement"].format(e=e, d=d) for e, d in zip(order, digits, strict=True)]
    try:
        return PV.statement_spans(text, ctx, facts)
    except ValueError:
        return []


def stage_examples(name: str, k: int, seed: int, group: str | None) -> None:
    from bridge_jspace.tokens import load_tokenizer

    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    chat.FORMAT = chat.manifest_format(m)  # the prompts shown exactly as the run fed them, whatever BJ_FORMAT says
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    try:
        tok = load_tokenizer()
    except Exception:
        tok = PV.tokenizer()
    items = {it["id"]: it for its in load_items(m).values() for it in its}
    primary = [la for la in m["windows"]["transit"] if la in m["layers"]]
    focus = group or "final"
    picked = [
        o for o in rows if o["source"] == "dissoc" and o["group"] == focus and o["layer"] in (*primary, "transit")
    ]
    if not picked:  # a smoke run without the transit layers: every dissoc row of the group
        picked = [o for o in rows if o["source"] == "dissoc" and o["group"] == focus and o["layer"] != 0]
    by_group: dict[str, list[dict]] = collections.defaultdict(list)
    for o in picked:
        g = o["role"] if o["role"] in ("position", *POINTER_ROLES, "identity", "value", "none", "context") else "other"
        by_group[g].append(o)
    by_group["same_changed"] = [
        o for o in rows if o["source"] == "same" and o["group"] == focus and o["role"] != "none"
    ]
    rng = random.Random(seed)
    unedited = {o["name"]: o for o in rows if o["source"] == "unedited"}
    examples = []
    for g, cand in by_group.items():
        for o in rng.sample(cand, min(k, len(cand))):
            it = items[o["name"]]
            prep = prepare(it, tok)
            text = prep["text"] + " "  # the read's prompt, exactly as fed: the space token appended
            sl, d = it["slots"], it["sources"]["dissoc"]
            st = statement_char_spans(prep["text"], it, it["entities"], it["digits"])
            q0 = prep["text"].rindex("\n" + it["question"]) + 1
            cue_at = prep["text"].find(it["cue"], q0)
            spans = [
                {"start": s, "end": e, "role": f"patched ({o['group']})"}
                for s, e in char_spans(prep["offsets"], prep["groups"][o["group"]])
            ]
            named = (("query", "bridge statement (base query, slot a)"),
                     ("identity", "identity statement (source's entity in the base)"),
                     ("position", "position statement (base entity at the source's queried slot)"),
                     ("end", "end statement (base statement at the source's slot counted from the end)"),
                     ("token", "token statement (base statement at the source statement's token offset)"),
                     ("back", "back statement (base statement as far back from the question as the source's)"))  # fmt: skip
            spans += [{"start": st[sl[key]][0], "end": st[sl[key]][1], "role": role} for key, role in named
                      if isinstance(sl.get(key), int) and sl[key] < len(st)]  # fmt: skip
            if cue_at >= 0:
                spans.append({"start": cue_at, "end": cue_at + len(it["cue"]), "role": "cue"})
            s_st = statement_char_spans(prep["source_text"], it, d["entities"], d["digits"])
            examples.append({
                "group": g, "family": it["family"], "item_id": it["id"], "domain": it["domain"], "prompt": text,
                "spans": spans,
                "source_prompt": prep["source_text"] + " ",
                "source_spans": [{"start": s_st[sl["position"]][0], "end": s_st[sl["position"]][1],
                                  "role": "source's queried statement (slot k)"}] if sl["position"] < len(s_st) else [],
                "condition": f"base's residual at the {o['group']} tokens replaced by the dissoc source's at layer "
                             f"{o['layer']} (one forward, answer read after 'Answer:' and a space)",
                "answers": {"clean": it["answer"], "edited": o["top"].strip(), "expected": d["predictions"],
                            "unedited_read": unedited[o["name"]]["top"].strip() if o["name"] in unedited else None},
                "numbers": {"p": o["p"], "layer": o["layer"], "role": o["role"]},
                "why": GROUP_DEFS[g] + f" ({o['top'].strip()!r})",
            })  # fmt: skip
    groups = [{"key": g, "title": g.replace("_", " "), "definition": GROUP_DEFS[g], "n_total": len(v)}
              for g, v in by_group.items()]  # fmt: skip
    out = {"exp": EXP, "run": name, "seed": seed, "k": k,
           "selection": f"source dissoc, group {focus}, layers {primary or 'all but 0'} and the transit window",
           "groups": groups, "examples": examples}  # fmt: skip
    (run_dir / "examples.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote", run_dir / "examples.json", len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["manifest", "run", "summarise", "examples", "analyze", "figures"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--data", default="pointer_v1", choices=list(DATASETS), help="the items' generator (data/<data>/)")
    ap.add_argument("--set", default="dev", help="a set of the --data generator (pointer_v1: main, dev, fit)")
    ap.add_argument("--levels", nargs="+", default=None, help="default: every level with files")
    ap.add_argument("--families", nargs="+", default=None, help="default: the generator's FAMILIES")
    ap.add_argument("--domains", nargs="+", default=None, help="default: the generator's DOMAINS")
    ap.add_argument(
        "--family-roles", nargs=3, default=None, help="primary, reference, contrast family (default per data)"
    )
    ap.add_argument("--n", type=int, default=25, help="scenes per (domain, base level)")
    ap.add_argument("--layers", nargs="+", type=int, default=None)
    ap.add_argument("--layer-step", type=int, default=2)
    ap.add_argument("--control-stride", type=int, default=2)
    ap.add_argument("--groups", nargs="+", default=None, choices=list(GROUPS), help="patch sites (default: all four)")
    ap.add_argument("--question-max-layer", type=int, default=None, help="patch the question words only up to here")
    ap.add_argument("--control-levels", nargs="+", default=None, help="levels that get the random and other controls")
    ap.add_argument(
        "--primary-layers",
        nargs="+",
        type=int,
        default=None,
        help="pointer_v4x's pre-registered layers on another target (default: the 27B's 48 and 50)",
    )
    ap.add_argument("--competence", default=None, help="the --data generator's competence run deciding eligibility")
    ap.add_argument("--no-eligibility", action="store_true", help="smoke runs: sample regardless of competence")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--seed", type=int, default=EXAMPLE_SEED)
    ap.add_argument("--group", default=None, choices=list(GROUPS))
    args = ap.parse_args()
    if args.stage == "manifest":
        assert args.why, "manifest needs --why"
        stage_manifest(args)
    elif args.stage == "run":
        stage_run(args.name)
    elif args.stage == "summarise":
        stage_summarise(args.name)
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k, args.seed, args.group)
