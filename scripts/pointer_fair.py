"""pointer_fair (D3b, batch 3, "fair C2"): at the depth where "lookups go around the lens" was measured, does a pointer
code steer the lookup where the lens push of the same size does not?

Background (UNVERIFIED): read_write (EXPERIMENTS rows 32, 37) found that at layers 32-40, on the tokens after the cue,
the J-lens reads a recalled bridge used for a lookup (memory → prompt) 95% of the time, but its push (bridge alt −
bridge org) switches <= 3% of answers at any size: "read without write". d3b_slot_direction_main_27b found that at
layer 48 a direction fitted to "which statement the question asks" (target minus current statement) does switch 37% of
memory → prompt answers where the lens push does not, but at another depth. This run puts both pushes in read_write's
cell, at the same sizes, aimed at the SAME answer: bridge alt's own statement digit.

Data and fits:
  pointer_v1 (animals, elements): memory → prompt (the lookup the claim is about), named → prompt (the entity named in
      the question), memory → memory (the null: nothing is looked up). The pointer direction is fitted on pointer_v1's
      fit set (memory → prompt; answered right; queried entity in a seeded half of each pool, as d3b_slot_direction_
      main_27b), per-token class means of the 5 asked statements at layers 32, 36, 40, at two token groups:
        after the cue   the question's last token ('?') and everything after it (instruction, template, 'Answer:'):
                        read_write's cell; the same tokens in every family, so one fit serves all three
        question words  the question's own tokens, cue included (memory → prompt only; one fit per topic, since the
                        cue phrases differ in length between topics)
  prompt → prompt (the animal suite, wording A: "Jack's pet is a cow. ... The cow's locker is 5. ... Which locker
      belongs to Jack's pet?"): its own pointer direction, per-token class means of the 3 locker statements on half the
      eligible scenes (seeded), pushed on the other half, at the tokens after the subject ('?' and after)
Pushes (added at the group's tokens; layers 32, 36, 40 one at a time and all three at once; 0.5, 1, 2, 4 times the
per-token size of the alt-prompt patch there: pointer_v1's alt prompt, the suite's C prompt):
  pointer   mean(bridge alt's statement) − mean(the asked statement), per token
  lens      the J++ direction v(bridge alt) − v(bridge org), the same at every token (read_write's push)
  random    a random direction per token, the pointer push's size;  shuffled: a direction fitted on shuffled labels
  patch     the alt prompt's hidden states pasted at those tokens (reference, not rescaled)
Both the pointer and the lens push predict the same answer: the digit of bridge alt's statement in the org prompt.
Every answer is also recorded as the index of the statement whose digit it is (for the overshoot analysis).
Intervals: an entity-cluster bootstrap (the queried entities resampled within each topic, 2000, seed 0); Wilson as well.

Decision rule (fixed before the 27B run). Deciding cell: memory → prompt, the tokens after the cue, layers 32, 36 and 40
at once, 1x the alt-prompt patch's size, topics pooled. "A pointer code steers the lookup where the lens push of the
same size does not, at the lens's depth" iff (a) the pointer push's rate of answers = bridge alt's statement digit has
an entity-bootstrap 95% lower bound >= 0.30, and (b) it exceeds both the lens push and the random push by >= 20 points
with each paired entity-bootstrap lower bound > 0. Valid only if the shuffled-label direction (memory → prompt) stays
at an upper bound <= 0.10 for that digit and the pointer push changes memory → memory answers with an upper bound
<= 0.10 (n >= 35 each). Second deciding cell, same rule: memory → prompt, the question words, layers 32-40 at once, 1x
(it says whether the pointer also acts at the question words). Reported, not decisive: each layer, each size, per
topic, named → prompt, prompt → prompt. Secondary, pre-registered (an exploratory post-hoc pattern on
d3b_slot_direction_main_27b): among the pointer push's answers in the deciding cell that are neither answer org nor the
target, the share on statements BEYOND the target (on the far side from the asked statement) against a uniform choice
among the off-target statements, and against the shuffled-label direction: "overshoot" iff the observed share exceeds
the uniform expectation with an entity-bootstrap lower bound > 0.
Decision rule, pointer_v4 additions (--data pointer_v4; fixed 2026-10-21 before any v4 run; batch 4, G2): why: the
pointer_v1 run failed its rule only through elements (6 entities; memory → memory changed 31% there, 2% in animals), so
it is rerun on pointer_v4 (three topics, countries / animals / body, 15-36 asked entities each, 3 statement x 3 question
wordings per topic). The fit uses pointer_v4's fit set only (fit entities, wordings 0-1: data/pointer_v4/split.json);
every pushed item (memory → prompt and memory → memory) has its asked entity or its wording held out of the fit (cut
entity, wording or both; never "neither"), all such items that pass the gate (every competence prompt right). Sizes 1x
and 2x; layers 32, 36, 40 one at a time and at once. Token groups: after the cue = the question's last token ('?') and
the 20 template tokens after it, as before, one per-token fit pooled over the topics (the same tokens in every topic,
wording and family); question words = the question's own tokens, whose number differs between wordings and entities, so
the pointer there is one vector per statement and layer (the mean over the question's tokens, pooled over the topics),
added at every question token at the patch's per-token size: reported, not decisive. Intervals: entity-cluster
bootstrap 95% (asked entity resampled within its topic, 2000, seed 0), widened to the item-level Wilson interval where
that is wider (rates; for differences the cluster bootstrap of the per-item paired difference); item-level next to it.
Deciding cell per topic: memory → prompt, after the cue, layers 32-40 at once, 1x. A topic passes iff (a) the pointer
push's rate of answers = bridge alt's statement digit has a lower bound >= 0.30 and (b) it exceeds the lens push and the
random push by >= 20 points, each paired difference's lower bound > 0; the topic counts only if valid: the
shuffled-label direction's rate there and the share of memory → memory answers the pointer push changes (same topic,
after the cue, layers 32-40, 1x) both keep an upper bound <= 0.10, n >= 35 each. "A pointer code steers the lookup where
the lens push of the same size cannot, at the lens's depth" iff >= 2 of the 3 topics pass and are valid. Flags reported
with it: pointer only later (pointer rate < 0.15 in >= 2 topics); not lookup-specific (memory → memory changed > 0.10 in
>= 2 topics). Reported, not decisive: topics pooled, each layer, 2x, the question words, per held-out cut, n items / k
entities / t wordings, the overshoot (pooled and per topic; the answer's statement index is recorded on every row).
Decision rule, transit sweep (--arms ... transit; fixed 2026-10-21 before any run with it; batch 4, after an outside
review): C2's kill test ("the lens push writes a lookup-used bridge at >= 3x random where the bridge is in transit")
fired on the pointer_v1 run's cell (elements, after the cue, 32-40, 1x: lens 30/150 vs random 2/150), but there the lens
push also wrote recall questions (memory → memory: 55/100), i.e. the bridge was still being recalled. "In transit" is
defined here, before the test. Sweep: memory → prompt and memory → memory items (the arm's items above), the tokens after
the cue, one layer at a time (28, 32, 36, 40, 44, 48, 52), the lens push (bridge alt − bridge org) and a random push at
1x and 4x the alt-prompt patch's per-token size, and the alt-prompt copy (the alt prompt's states pasted; not rescaled).
Rates: lens / random = answers that become bridge alt's answer (memory → prompt: bridge alt's statement digit; memory →
memory: bridge alt's recalled fact); copy = memory → prompt answers changed (any answer but the unedited one).
Intervals as the pointer_v4 rule (entity-cluster, widened to Wilson; differences: cluster bootstrap of paired items).
Per topic and size (primary 1x; 4x reported the same way): a layer is in transit iff the memory → memory lens rate's
upper bound <= 2x the memory → memory random rate's upper bound (so with no random hits, the lens may not exceed about
2x the one-hit level either) and the copy changes >= 50% of memory → prompt answers (point estimate). C2 at a transit
layer: holds iff the memory → prompt lens rate is < 3x the random rate (point estimates) or its upper bound < 0.10;
otherwise killed iff the paired lens − random difference has a lower bound > 0; otherwise unclear. Per topic: not
testable (no transit layer), killed (killed at any transit layer), holds (holds at every transit layer), else undecided.
Hypotheses reported as flags: H-C2-transit (>= 2 topics have transit layers, none is killed and every testable topic
holds), H-no-transit (some topic has no transit layer), H-C2-killed (some topic killed).

Stages:  run --name N --why W [--data pointer_v4 --competence RUN] [...]   analyze --name N   figures --name N
         examples --name N [--k 3]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from bridge_jspace.stats import wilson
from bridge_jspace.tokens import raw_encoding
from scripts import pointer_fit as PF
from scripts import pointer_probe as PP
from scripts import pointer_swap as PS
from scripts import suite_split as SP
from scripts import suite_v1 as S

EXP = "pointer_fair"
RESULTS = pins.RESULTS_DIR / EXP
DEFAULTS: dict[str, Any] = {
    "data": "pointer_v1", "domains": ["animals", "elements"], "layers": [32, 36, 40], "scales": [0.5, 1.0, 2.0, 4.0],
    "n": {"RL": 150, "DL": 100, "RR": 100, "BL": 400}, "competence": "d3b_competence_400", "suite": True,
    "primary_scale": 1.0, "fit_limit": None, "arms": ["pointer"], "transit_layers": [28, 32, 36, 40, 44, 48, 52],
    "transit_scales": [1.0, 4.0],
}  # fmt: skip
# pointer_v4: every held-out eligible item (<= 212 per topic and family), no named → prompt, no animal suite; both arms
V4_DEFAULTS: dict[str, Any] = {"scales": [1.0, 2.0], "n": {"RL": 250, "DL": 0, "RR": 250, "BL": 0}, "suite": False,
                               "arms": ["pointer", "transit"]}  # fmt: skip
ARMS = ("pointer", "transit")
TRANSIT = "transit"  # the outcome rows' group of the transit sweep (its tokens: after the cue)
RR_MAX_RATIO, COPY_MIN, KILL_RATIO, NEGLIGIBLE = 2.0, 0.50, 3.0, 0.10
CONDS = ("pointer", "lens", "random", "shuffled")
SPLIT_SEED, SHUFFLE_SEED, SAMPLE_SEED, NULL_SEED, BOOT_SEED, N_BOOT, EXAMPLE_SEED = 0, 1, 0, 0, 0, 2000, 0
RATE_MIN, MARGIN, CONTROL_MAX, LATER_MAX, MIN_TOPICS = 0.30, 0.20, 0.10, 0.15, 2
FAMILY_WORDS = {"RL": "memory → prompt", "DL": "named → prompt", "RR": "memory → memory", "BL": "prompt → prompt"}
CUTS = ("entity", "template", "both")
CUT_WORDS = {"entity": "asked entity held out", "template": "wording held out", "both": "both held out"}
BATCH = PS.BATCH
LOCKER = re.compile(r"The (\w+)'s locker is (\d)\.")


# ---- pure helpers (tests/test_pointer_fair.py) ---------------------------------------------------------------------


def after_group(question: list[int], final: list[int]) -> list[int]:
    """The question's last token ('?') and every token after it: read_write's cell, the same in every family."""
    return question[-1:] + final


def locker_order(context: str) -> list[tuple[str, str]]:
    """(animal, digit) of the animal suite's locker statements, in the order the context states them."""
    return LOCKER.findall(context)


def beyond(a: int, j: int, k: int) -> bool:
    """Is statement k beyond the target j, on the far side from the asked statement a?"""
    return k > j if j > a else k < j


def overshoot_expectation(a: int, j: int, n: int) -> float:
    """Share of the off-target statements (not a, not j) that lie beyond j: the uniform null for one off-target answer."""
    off = [k for k in range(n) if k not in (a, j)]
    return sum(beyond(a, j, k) for k in off) / len(off) if off else math.nan


def answer_slot(digit: str | None, digits: list[str]) -> int | None:
    return digits.index(digit) if digit is not None and digit in digits else None


def is_v4(cfg: dict) -> bool:
    return cfg.get("data") == "pointer_v4"


def window_key(layers: list[int] | tuple[int, ...]) -> str:
    """The label of 'all pushed layers at once' ('32-40' for 32, 36, 40: the key of every earlier run)."""
    return f"{min(layers)}-{max(layers)}"


def widen(boot: list[float], wil: list[float]) -> list[float]:
    """[rate, lo, hi]: the entity-cluster interval widened to the item-level Wilson interval where that is wider (at 0
    or n hits every resample agrees, and the Wilson interval stands)."""
    if any(math.isnan(v) for v in (*boot, *wil)):
        return [math.nan] * 3
    return [boot[0], min(boot[1], wil[1]), max(boot[2], wil[2])]


def families(cfg: dict) -> list[str]:
    return [f for f in ("RL", "DL", "RR") if cfg["n"].get(f, 0) > 0]


def arms_of(cfg: dict) -> list[str]:
    """The run's arms (runs before batch 4 had only the pointer arm)."""
    return list(cfg.get("arms", ["pointer"]))


def in_transit(rr_lens_hi: float, rr_random_hi: float, copy_changed: float) -> bool:
    """A layer is in transit for a topic iff the lens push no longer writes the recalled fact on memory → memory
    (upper bound of its rate <= 2x the random push's upper bound) while the alt-prompt copy there still changes >= 50%
    of memory → prompt answers (docstring)."""
    return rr_lens_hi <= RR_MAX_RATIO * rr_random_hi and copy_changed >= COPY_MIN


def c2_layer(lens: list[float], random_: list[float], diff_lo: float) -> str:
    """C2 at one transit layer, memory → prompt: 'holds' iff the lens push's rate is < 3x the random push's or its upper
    bound < 10%; else 'killed' iff the paired lens − random difference has a lower bound > 0; else 'unclear'."""
    if lens[0] < KILL_RATIO * random_[0] or lens[2] < NEGLIGIBLE:
        return "holds"
    return "killed" if diff_lo > 0 else "unclear"


def c2_topic(layer_verdicts: list[str]) -> str:
    """'not testable' (no transit layer), 'killed' (any layer), 'holds' (every layer), else 'undecided'."""
    if not layer_verdicts:
        return "not testable"
    if "killed" in layer_verdicts:
        return "killed"
    return "holds" if all(v == "holds" for v in layer_verdicts) else "undecided"


def topic_verdict(ptr_lo: float, d_lens: list[float], d_rand: list[float], shuf_hi: float, shuf_n: int, rr_hi: float,
                  rr_n: int) -> tuple[bool, bool]:  # fmt: skip
    """(passes, valid) of one deciding cell: rule (a) and (b), and the two controls (docstring)."""
    passes = ptr_lo >= RATE_MIN and min(d_lens[0], d_rand[0]) >= MARGIN and min(d_lens[1], d_rand[1]) > 0
    valid = shuf_n >= 35 and shuf_hi <= CONTROL_MAX and rr_n >= 35 and rr_hi <= CONTROL_MAX
    return passes, valid


# ---- items ----------------------------------------------------------------------------------------------------------


def v1_items(cfg: dict) -> list[dict]:
    """The pushed items: eligible main items per family and topic, seeded; pointer_v4: only items whose asked entity or
    wording the fit never saw (cut != 'neither')."""
    G = PF.data_gen(cfg)
    good = PF.eligible_main(cfg["competence"], cfg) if cfg["competence"] else None
    rng = random.Random(SAMPLE_SEED)
    out = []
    for fam in ("RL", "DL", "RR"):
        for d in cfg["domains"]:
            its = [
                it
                for it in PF.PV.load_file(G.DATA / "main" / f"{d}_{fam}_e5f0.json")
                if (good is None or it["id"] in good) and (not is_v4(cfg) or it["cut"] != "neither")
            ]
            out += [its[i] for i in sorted(rng.sample(range(len(its)), min(cfg["n"].get(fam, 0), len(its))))]
    return out


def suite_items(cfg: dict, tok) -> tuple[list[dict], list[dict]]:
    """The animal suite's prompt → prompt items (eligible), prepared, split into (fit half, push half) by scene."""
    its = S.load("BL", "A")
    if cfg["competence"]:
        ok: dict[str, list[bool]] = collections.defaultdict(list)
        for line in SP.competence_file("BL", "A").read_text().splitlines():
            r = json.loads(line)
            if r["family"] == "BL":
                ok[r["id"]].append(r["correct"])
        its = [it for it in its if ok.get(it["id"]) and all(ok[it["id"]])]
    its = its[: cfg["n"]["BL"]]
    out = []
    for it in its:
        c = {**it, **SP.prepare(it, tok)}
        rendered = S.render(tok, it["context"], it["question"])
        offs = raw_encoding(tok, rendered, offsets=True)["offset_mapping"]
        q0 = rendered.rindex("\n" + it["question"]) + 1
        q1 = q0 + len(it["question"])
        question = [i for i, (s, e) in enumerate(offs) if e > q0 and s < q1]
        final = [i for i, (s, _) in enumerate(offs) if s >= q1]
        order = locker_order(it["context"])
        animals = [a for a, _ in order]
        c |= {"after": after_group(question, final), "text": rendered, "offsets": [list(o) for o in offs],
              "locker_digits": [dg for _, dg in order], "asked": animals.index(it["bridge"]),
              "target": animals.index(it["cf_bridge"]), "query": it["bridge"], "alt_query": it["cf_bridge"],
              "domain": "animals"}  # fmt: skip
        out.append(c)
    names = sorted({c["scene"] for c in out})
    random.Random(SPLIT_SEED).shuffle(names)
    fit_scenes = set(names[: len(names) // 2])
    return [c for c in out if c["scene"] in fit_scenes], [c for c in out if c["scene"] not in fit_scenes]


def input_files(cfg: dict) -> list[Path]:
    G = PF.data_gen(cfg)
    files = [G.DATA / "fit" / f"{d}_RL_e5f0.json" for d in cfg["domains"]]
    files += [G.DATA / "main" / f"{d}_{f}_e5f0.json" for d in cfg["domains"] for f in families(cfg)]
    if is_v4(cfg):
        files.append(G.split_file())
    if cfg["competence"]:
        files.append(G.RESULTS / cfg["competence"] / "items.jsonl")
    if cfg["suite"]:
        files.append(S.DATA / "BL.json")
        if cfg["competence"]:
            files.append(SP.competence_file("BL", "A"))
    return files


# ---- the run ----------------------------------------------------------------------------------------------------------


def fit_means(x: torch.Tensor, y: torch.Tensor, y_shuf: torch.Tensor, n_classes: int) -> dict[str, Any]:
    mu, m = PF.class_means(x, y, n_classes)
    mu_s, _ = PF.class_means(x, y_shuf, n_classes)
    return {"mu": mu, "m": m, "mu_shuf": mu_s}


def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows

    pins.check_run_name(name)
    assert cfg["primary_scale"] in cfg["scales"], "the primary size must be one of the sizes"
    assert "transit" not in arms_of(cfg) or cfg["primary_scale"] in cfg["transit_scales"], "primary size not swept"
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    doc = __doc__ or ""
    v4 = is_v4(cfg)
    manifest = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": pins.model_pin(), "switches": switches(), "lens": [pins.FROZEN_LENS, pins.FROZEN_LENS_SHA256], "config": cfg,
                "inputs": {PF.rel(p): sha256_of(p) for p in input_files(cfg)},
                "entity_split": {d: {"fit": a, "held_out": b} for d, (a, b) in PF.pools(cfg).items()},
                "ci": PS.CLUSTER_CI if v4 else {"kind": "entity-cluster bootstrap; Wilson reported next to it"},
                "seeds": {"split": SPLIT_SEED, "shuffle": SHUFFLE_SEED, "sample": SAMPLE_SEED, "null": NULL_SEED,
                          "bootstrap": BOOT_SEED, "examples": EXAMPLE_SEED},
                "design": doc.split("Decision rule")[0], "decision": "Decision rule" + doc.split("Decision rule")[1].split("Stages:")[0]}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    t0 = time.time()
    arms = arms_of(cfg)
    layers = tuple(cfg["layers"])
    t_layers = tuple(cfg["transit_layers"]) if "transit" in arms else ()
    rec_layers = tuple(sorted(set(layers if "pointer" in arms else ()) | set(t_layers)))
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    split = PF.pools(cfg)
    # 1. the fit (after the cue: per token, pooled over the topics; question words: per token and topic, or pointer_v4:
    # the mean over the question's tokens, pooled over the topics); the transit sweep needs none
    feats: dict[tuple[str, str], dict[int, list[torch.Tensor]]] = collections.defaultdict(
        lambda: {la: [] for la in layers}
    )
    labels: dict[tuple[str, str], list[int]] = collections.defaultdict(list)
    preps = [(it, PS.prepare(it, tok)) for it in PF.fit_items(cfg)] if "pointer" in arms else []
    by_len: dict[int, list[tuple[dict, dict]]] = collections.defaultdict(list)
    for it, p in preps:
        by_len[len(p["read_ids"]["base"])].append((it, p))
    for chunk in progress([g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)], "fit collect"):
        logits, rec = forward_rows(model, torch.tensor([p["read_ids"]["base"] for _, p in chunk], device="cuda"),
                                   [{}] * len(chunk), layers)  # fmt: skip
        for ri, (it, p) in enumerate(chunk):
            right = digit_tok.get(int(logits[ri].argmax())) == it["answer"]
            if (cfg.get("require_correct", True) and not right) or it["query"] not in split[it["domain"]][0]:
                continue
            g = p["groups"]
            for key, pos in (
                (("after", "all"), after_group(g["question"], g["final"])),
                (("question", "all" if v4 else it["domain"]), g["question"]),
            ):
                for la in layers:
                    h = rec[la][ri, pos]
                    feats[key][la].append((h.float().mean(0) if v4 and key[0] == "question" else h).half().cpu())
                labels[key].append(it["slots"]["query"])
    fits: dict[tuple[str, str], dict[int, dict[str, Any]]] = {}
    fit_info = []
    gen_s = torch.Generator().manual_seed(SHUFFLE_SEED)
    for key in feats:
        y = torch.tensor(labels[key], device="cuda")
        y_s = y[torch.randperm(len(y), generator=gen_s).to(y.device)]
        fits[key] = {la: fit_means(torch.stack(feats[key][la]).cuda().float(), y, y_s, PF.N_SLOTS) for la in layers}
        fit_info.append(
            {
                "group": key[0],
                "topic": key[1],
                "n": len(y),
                "per_statement": [int((y == c).sum()) for c in range(PF.N_SLOTS)],
            }
        )
    # 2. the animal suite's prompt → prompt fit (3 locker statements)
    bl_fit, bl_push = suite_items(cfg, tok) if cfg["suite"] and "pointer" in arms else ([], [])
    if bl_fit:
        fx: dict[int, list[torch.Tensor]] = {la: [] for la in layers}
        fy = []
        for c in progress(bl_fit, "suite fit collect"):
            _, rec = forward_rows(model, torch.tensor([c["read_ids"]["clean"]], device="cuda"), [{}], layers)
            for la in layers:
                fx[la].append(rec[la][0, c["after"]].half().cpu())
            fy.append(c["asked"])
        y = torch.tensor(fy, device="cuda")
        y_s = y[torch.randperm(len(y), generator=gen_s).to(y.device)]
        fits[("after", "suite")] = {la: fit_means(torch.stack(fx[la]).cuda().float(), y, y_s, 3) for la in layers}
        fit_info.append(
            {"group": "after", "topic": "suite", "n": len(fy), "per_statement": [int((y == c).sum()) for c in range(3)]}
        )
    (out_dir / "fit.json").write_text(json.dumps({"fits": fit_info}, indent=2) + "\n")
    # 3. pushes
    out_f = open(out_dir / "outcomes.jsonl", "w")  # noqa: SIM115 - appended item by item, closed below
    cases: list[dict] = []
    n_rows = 0
    settings: list[tuple[Any, tuple[int, ...]]] = [(la, (la,)) for la in layers] + [(window_key(layers), layers)]
    todo = [("v1", c) for c in v1_items(cfg)] + [("suite", c) for c in bl_push]
    for ci, (src, c) in enumerate(progress(todo, "push")):
        wording = PS.wording_of(c)  # pointer_v4: the wording and the held-out cut; else {}
        if src == "v1":
            p = PS.prepare(c, tok)
            g = p["groups"]
            after_pos = after_group(g["question"], g["final"])
            groups = {"after": after_pos} if "pointer" in arms else {}
            if "pointer" in arms and (c["family"] == "RL" or v4):  # pointer_v4: memory → memory too (its control)
                groups["question"] = g["question"]
            ids = [p["read_ids"]["base"], p["read_ids"]["dissoc"]]
            a, j = c["slots"]["query"], c["slots"]["identity"]
            digits = [str(d) for d in c["digits"]]
            target_digit, org = c["sources"]["dissoc"]["predictions"]["identity"], c["answer"]
            q_b, q_s = c["query"], c["sources"]["dissoc"]["query"]
            fit_key = {"after": ("after", "all"), "question": ("question", "all" if v4 else c["domain"])}
            text, offsets = p["text"], p["offsets"]
        else:
            after_pos = c["after"]
            groups = {"after": after_pos}
            ids = [c["read_ids"]["clean"], c["read_ids"]["cf"]]
            a, j = c["asked"], c["target"]
            digits = c["locker_digits"]
            target_digit, org = c["cf_answer"], c["answer"]
            q_b, q_s = c["bridge"], c["cf_bridge"]
            fit_key = {"after": ("after", "suite")}
            text, offsets = c["text"], c["offsets"]
        _, rec = forward_rows(model, torch.tensor(ids, device="cuda"), [{}, {}], rec_layers)
        pair = torch.tensor([model.concept_token(q_b), model.concept_token(q_s)], device="cuda")
        lens_dir = {la: (lambda v: v[1] - v[0])(lens.vectors(la, pair)) for la in rec_layers}
        gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 1_000_003 * ci)
        jobs: list[tuple[dict, dict]] = [({"cond": "unedited", "group": None, "layer": None, "scale": None}, {})]
        for gname, pos in groups.items():
            ft = fits[fit_key[gname]]
            vec: dict[tuple[int, float, str], torch.Tensor] = {}
            for la in layers:
                size = (rec[la][1, pos] - rec[la][0, pos]).norm(dim=-1)
                for sc in cfg["scales"]:
                    pv = PF.matched(ft[la]["mu"][j] - ft[la]["mu"][a], sc * size)
                    vec[(la, sc, "pointer")] = pv
                    vec[(la, sc, "lens")] = PF.matched(lens_dir[la], sc * size)
                    vec[(la, sc, "random")] = PS.null_rows(pv, gen)
                    vec[(la, sc, "shuffled")] = PF.matched(ft[la]["mu_shuf"][j] - ft[la]["mu_shuf"][a], sc * size)
            for key, lay in settings:
                jobs.append(({"cond": "patch", "group": gname, "layer": key, "scale": None},
                             {la: PS.SetRows(rec[la][1, pos], pos) for la in lay}))  # fmt: skip
                for sc in cfg["scales"]:
                    for cn in CONDS:
                        jobs.append(({"cond": cn, "group": gname, "layer": key, "scale": sc},
                                     {la: PS.AddRows(vec[(la, sc, cn)], pos) for la in lay}))  # fmt: skip
        if src == "v1":  # the transit sweep: one layer at a time, after the cue, lens and random push, alt-prompt copy
            for la in t_layers:
                size = (rec[la][1, after_pos] - rec[la][0, after_pos]).norm(dim=-1)
                tag = {"group": TRANSIT, "layer": la}
                jobs.append(
                    ({**tag, "cond": "patch", "scale": None}, {la: PS.SetRows(rec[la][1, after_pos], after_pos)})
                )
                for sc in cfg["transit_scales"]:
                    lv = PF.matched(lens_dir[la], sc * size)
                    for cn, v in (("lens", lv), ("random", PS.null_rows(lv, gen))):
                        jobs.append(({**tag, "cond": cn, "scale": sc}, {la: PS.AddRows(v, after_pos)}))
        read = torch.tensor([ids[0]], device="cuda")
        base_top = -1
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            logits, _ = forward_rows(model, read, [e for _, e in chunk])
            for ri, (tags, _) in enumerate(chunk):
                top = int(logits[ri].argmax())
                if tags["cond"] == "unedited":
                    base_top = top
                dg = digit_tok.get(top)
                role = ("target" if dg == target_digit else "org" if dg == org else "context" if dg in digits else
                        "other_digit" if dg is not None else "other")  # fmt: skip
                out_f.write(json.dumps({"family": c["family"], "domain": c["domain"], "name": c["id"], "query": q_b,
                                        **wording, "asked": a, "target_slot": j, "n_statements": len(digits), **tags,
                                        "top": tok.decode([top]).strip(), "role": role, "changed": top != base_top,
                                        "answer_slot": answer_slot(dg, digits)}) + "\n")  # fmt: skip
                n_rows += 1
        cases.append({"id": c["id"], "family": c["family"], "domain": c["domain"], "query": q_b, "alt_query": q_s,
                      **wording, "asked": a, "target_slot": j, "digits": digits, "answer": org,
                      "target_digit": target_digit, "text": text, "context": c["context"], "question": c["question"],
                      "groups_chars": {gname: [offsets[pos[0]][0], offsets[pos[-1]][1]]
                                       for gname, pos in {"after": after_pos, **groups}.items()}})  # fmt: skip
    out_f.close()
    PF.write_rows(out_dir / "cases.jsonl", cases)
    sm = summarise(load_rows(name), cfg)
    sm |= {"seconds": round(time.time() - t0), "edited_reads": n_rows}
    (out_dir / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(sm))
    print((out_dir / "summary.md").read_text())


def load_rows(name: str) -> list[dict]:
    return [json.loads(x) for x in (RESULTS / name / "outcomes.jsonl").read_text().splitlines()]


# ---- analysis ---------------------------------------------------------------------------------------------------------


def sel(rows: list[dict], **where) -> dict[str, dict]:
    return {o["name"]: o for o in rows if all(o.get(k) == v for k, v in where.items())}


def stat(c: dict[str, dict], key: str = "role", value: Any = "target") -> dict[str, Any]:
    """Rate of rows with row[key] == value: Wilson, entity-cluster bootstrap, the latter widened to Wilson ('ci', the
    interval pointer_v4's rule reads), n items, k entities, t wordings (pointer_v4)."""
    rows = list(c.values())
    hits = [float(o[key] == value) for o in rows]
    wil = [round(v, 4) for v in wilson(int(sum(hits)), len(rows))] if rows else [math.nan] * 3
    boot = [round(v, 4) for v in PP.entity_boot(hits, [o["domain"] for o in rows], [o["query"] for o in rows])]
    return {"n": len(rows), "k_entities": len({(o["domain"], o["query"]) for o in rows}),
            "t_wordings": len({(o["domain"], o["template"]) for o in rows if "template" in o}),
            "wilson": wil, "entity_boot": boot, "ci": widen(boot, wil)}  # fmt: skip


def paired_diff(c1: dict[str, dict], c2: dict[str, dict]) -> list[float]:
    names = sorted(set(c1) & set(c2))
    d = [float(c1[n]["role"] == "target") - float(c2[n]["role"] == "target") for n in names]
    return [round(v, 4) for v in PP.entity_boot(d, [c1[n]["domain"] for n in names], [c1[n]["query"] for n in names])]


def overshoot(c: dict[str, dict]) -> dict[str, Any]:
    """Off-target answers (a statement's digit, not answer org, not the target): share beyond the target vs uniform."""
    rows = [
        o for o in c.values() if o["answer_slot"] is not None and o["answer_slot"] not in (o["asked"], o["target_slot"])
    ]
    obs = [float(beyond(o["asked"], o["target_slot"], o["answer_slot"])) for o in rows]
    exp = [overshoot_expectation(o["asked"], o["target_slot"], o["n_statements"]) for o in rows]
    diff = PP.entity_boot(
        [x - e for x, e in zip(obs, exp, strict=True)], [o["domain"] for o in rows], [o["query"] for o in rows]
    )
    return {"n_off_target": len(rows), "beyond": int(sum(obs)), "expected_uniform": round(float(sum(exp)), 2),
            "beyond_minus_uniform": [round(v, 4) for v in diff]}  # fmt: skip


def overshoot_by_topic(c: dict[str, dict], topics: list[str]) -> dict[str, Any]:
    out = {"pooled": overshoot(c)}
    for t in topics:
        out[t] = overshoot({n: o for n, o in c.items() if o["domain"] == t})
    return out


def decide_v4(rows: list[dict], cfg: dict) -> dict[str, Any]:
    """pointer_v4's rule (docstring): per topic, then >= 2 of 3 topics; the question words reported the same way."""
    sc, win, topics = cfg["primary_scale"], window_key(cfg["layers"]), list(cfg["domains"])
    unedited = [o for o in rows if o["cond"] == "unedited"]
    out: dict[str, Any] = {"window": win, "unedited_answer_org": {fam: stat(sel(unedited, family=fam), "role", "org")
                                                   for fam in sorted({o["family"] for o in unedited})}}  # fmt: skip
    for group in ("after", "question"):

        def c(cond: str, fam: str = "RL", topic: str | None = None, group: str = group, scale: Any = sc):
            where = {"family": fam, "group": group, "layer": win, "scale": scale, "cond": cond}
            return sel(rows, **where, **({"domain": topic} if topic else {}))

        if not c("pointer"):
            continue
        per: dict[str, Any] = {}
        for t in [*topics, None]:
            ptr = c("pointer", topic=t)
            cell = {cn: stat(c(cn, topic=t)) for cn in CONDS}
            rr = {cn: stat(c(cn, "RR", t), "changed", True) for cn in CONDS}
            d_lens, d_rand = paired_diff(ptr, c("lens", topic=t)), paired_diff(ptr, c("random", topic=t))
            passes, valid = topic_verdict(cell["pointer"]["ci"][1], d_lens, d_rand, cell["shuffled"]["ci"][2],
                                          cell["shuffled"]["n"], rr["pointer"]["ci"][2], rr["pointer"]["n"])  # fmt: skip
            per[t or "pooled"] = {**cell, "memory_memory_changed": rr["pointer"], "memory_memory_changed_by": rr,
                                  "pointer_minus_lens": d_lens, "pointer_minus_random": d_rand,
                                  "patch": stat(c("patch", topic=t, scale=None)),
                                  "pointer_2x": stat(c("pointer", topic=t, scale=2.0)) if c("pointer", topic=t, scale=2.0) else None,
                                  "lens_2x": stat(c("lens", topic=t, scale=2.0)) if c("lens", topic=t, scale=2.0) else None,
                                  "passes": passes, "valid": valid}  # fmt: skip
        n_ok = sum(per[t]["passes"] and per[t]["valid"] for t in topics)
        flags = {"pointer_at_lens_depth": n_ok >= MIN_TOPICS,
                 "pointer_later_only": sum(per[t]["pointer"]["ci"][0] < LATER_MAX for t in topics) >= MIN_TOPICS,
                 "not_lookup_specific": sum(per[t]["memory_memory_changed"]["ci"][0] > CONTROL_MAX for t in topics) >= MIN_TOPICS}  # fmt: skip
        per_cut = {cut: {cn: stat({n: o for n, o in c(cn).items() if o.get("cut") == cut}) for cn in ("pointer", "lens")}
                   for cut in CUTS}  # fmt: skip
        verdict = (f"the pointer steers where the lens push does not, in {n_ok} of {len(topics)} topics" if n_ok >= MIN_TOPICS
                   else f"not shown: {n_ok} of {len(topics)} topics pass with valid controls (needs {MIN_TOPICS})")  # fmt: skip
        out[group] = {"decisive": group == "after", "topics": per, "topics_passing": n_ok, "flags": flags,
                      "verdict": verdict, "per_cut": per_cut,
                      "overshoot": overshoot_by_topic(c("pointer"), topics),
                      "overshoot_shuffled": overshoot_by_topic(c("shuffled"), topics)}  # fmt: skip
    return out


def decide_transit(rows: list[dict], cfg: dict) -> dict[str, Any]:
    """The transit sweep's rule (docstring): per size and topic, the transit layers and C2 there; flags per size."""
    topics = list(cfg["domains"])
    out: dict[str, Any] = {"layers": cfg["transit_layers"], "primary_scale": cfg["primary_scale"], "by_scale": {}}
    for s in cfg["transit_scales"]:
        per: dict[str, Any] = {}
        for t in topics:
            table, verdicts = [], []
            for la in cfg["transit_layers"]:

                def c(cond: str, fam: str, scale: Any = s, la: int = la, t: str = t) -> dict[str, dict]:
                    return sel(rows, family=fam, group=TRANSIT, layer=la, scale=scale, cond=cond, domain=t)

                rl_lens, rl_rand = c("lens", "RL"), c("random", "RL")
                r = {"layer": la, "rl_lens": stat(rl_lens), "rl_random": stat(rl_rand),
                     "rl_copy_changed": stat(c("patch", "RL", None), "changed", True),
                     "rl_copy_target": stat(c("patch", "RL", None)), "rr_lens": stat(c("lens", "RR")),
                     "rr_random": stat(c("random", "RR")), "rr_copy_changed": stat(c("patch", "RR", None), "changed", True),
                     "rl_lens_minus_random": paired_diff(rl_lens, rl_rand)}  # fmt: skip
                r["transit"] = bool(r["rr_lens"]["n"] and r["rl_copy_changed"]["n"]) and in_transit(
                    r["rr_lens"]["ci"][2], r["rr_random"]["ci"][2], r["rl_copy_changed"]["ci"][0]
                )
                r["c2"] = (
                    c2_layer(r["rl_lens"]["ci"], r["rl_random"]["ci"], r["rl_lens_minus_random"][1])
                    if r["transit"]
                    else None
                )
                verdicts += [r["c2"]] if r["transit"] else []
                table.append(r)
            per[t] = {
                "layers": table,
                "transit_layers": [r["layer"] for r in table if r["transit"]],
                "c2": c2_topic(verdicts),
            }
        testable = [t for t in topics if per[t]["c2"] != "not testable"]
        flags = {"c2_transit": len(testable) >= MIN_TOPICS and all(per[t]["c2"] == "holds" for t in testable),
                 "no_transit": len(testable) < len(topics), "c2_killed": any(per[t]["c2"] == "killed" for t in topics)}  # fmt: skip
        out["by_scale"][f"{s:g}"] = {"topics": per, "flags": flags}
    return out


def summarise(rows: list[dict], cfg: dict) -> dict:
    sc = cfg["primary_scale"]
    win = window_key(cfg["layers"])
    out: dict[str, Any] = {"cells": {}}
    if "transit" in arms_of(cfg):
        out["transit"] = decide_transit(rows, cfg)
    grouped: dict[tuple, dict[str, dict]] = collections.defaultdict(dict)
    for o in rows:
        if o["cond"] != "unedited":
            grouped[(o["family"], o["group"], o["layer"], o["scale"], o["cond"])][o["name"]] = o
    for (fam, group, layer, scale, cond), rows_c in grouped.items():
        cell = {"target": stat(rows_c), "changed": stat(rows_c, "changed", True)}
        for dom in sorted({o["domain"] for o in rows_c.values()}):
            cell[f"target:{dom}"] = stat({n: o for n, o in rows_c.items() if o["domain"] == dom})
            cell[f"changed:{dom}"] = stat({n: o for n, o in rows_c.items() if o["domain"] == dom}, "changed", True)
        out["cells"][f"{fam}|{group}|{layer}|{scale}|{cond}"] = cell
    if is_v4(cfg):
        out["v4"] = decide_v4(rows, cfg)
        return out
    decisions = {}
    for group in ("after", "question"):

        def c(cond: str, fam: str = "RL", group: str = group) -> dict[str, dict]:
            return sel(rows, family=fam, group=group, layer=win, scale=sc, cond=cond)

        if not c("pointer"):
            continue
        ptr = stat(c("pointer"))
        d_lens, d_rand = paired_diff(c("pointer"), c("lens")), paired_diff(c("pointer"), c("random"))
        shuf = stat(c("shuffled"))
        rr = stat(sel(rows, family="RR", group="after", layer=win, scale=sc, cond="pointer"), "changed", True)
        ok = (
            ptr["entity_boot"][1] >= RATE_MIN
            and d_lens[0] >= MARGIN
            and d_rand[0] >= MARGIN
            and d_lens[1] > 0
            and d_rand[1] > 0
        )
        valid = (
            shuf["entity_boot"][2] <= CONTROL_MAX
            and shuf["n"] >= 35
            and rr["entity_boot"][2] <= CONTROL_MAX
            and rr["n"] >= 35
        )
        decisions[group] = {"pointer": ptr, "lens": stat(c("lens")), "random": stat(c("random")), "shuffled": shuf,
                            "memory_memory_changed": rr, "pointer_minus_lens": d_lens, "pointer_minus_random": d_rand,
                            "patch": stat(sel(rows, family="RL", group=group, layer=win, scale=None, cond="patch")),
                            "overshoot": overshoot(c("pointer")), "overshoot_shuffled": overshoot(c("shuffled")),
                            "verdict": ("the pointer steers where the lens push does not" if ok else "not shown")
                            + ("" if valid else " (controls failed or n too small: not interpretable)")}  # fmt: skip
    out["decisions"] = decisions
    return out


def pct(b: list[float]) -> str:
    return "-" if math.isnan(b[0]) else f"{100 * b[0]:.0f}% [{100 * b[1]:.0f}, {100 * b[2]:.0f}]"


def pts(b: list[float]) -> str:
    return "-" if math.isnan(b[0]) else f"{100 * b[0]:+.0f} [{100 * b[1]:+.0f}, {100 * b[2]:+.0f}]"


def summary_md_v4(v4: dict) -> str:
    def nkt(x: dict) -> str:
        return f"{x['n']} / {x['k_entities']} / {x['t_wordings']}"

    lines = [f"# {EXP} (pointer_v4)", "", "Intervals: entity-cluster bootstrap 95% (asked entity within its topic), widened "
             "to Wilson where wider; 'item level': Wilson alone. n items / k entities / t wordings.", "",
             "Unedited answers = answer org: " + "; ".join(f"{FAMILY_WORDS[f]} {pct(x['ci'])} (n={x['n']})"
                                                         for f, x in v4["unedited_answer_org"].items()), ""]  # fmt: skip
    for group in ("after", "question"):
        d = v4.get(group)
        if not d:
            continue
        where = "after the cue" if group == "after" else "question words (reported, not decisive)"
        lines += [f"## memory → prompt, {where}, layers {v4['window']} at once, 1x: **{d['verdict']}**", "",
                  f"Flags: {json.dumps(d['flags'])}", "",
                  "| topic | pointer | item level | lens | random | shuffled | memory → memory changed (pointer) | "
                  "pointer − lens | pointer − random | pointer 2x | lens 2x | passes / valid | n / k / t |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
        for t, x in d["topics"].items():
            mm = x["memory_memory_changed"]
            lines.append(f"| {t} | {pct(x['pointer']['ci'])} | {pct(x['pointer']['wilson'])} | {pct(x['lens']['ci'])} | "
                         f"{pct(x['random']['ci'])} | {pct(x['shuffled']['ci'])} | {pct(mm['ci'])} (n={mm['n']}) | "
                         f"{pts(x['pointer_minus_lens'])} | {pts(x['pointer_minus_random'])} | "
                         f"{pct(x['pointer_2x']['ci']) if x['pointer_2x'] else '-'} | "
                         f"{pct(x['lens_2x']['ci']) if x['lens_2x'] else '-'} | {x['passes']} / {x['valid']} | "
                         f"{nkt(x['pointer'])} |")  # fmt: skip
        lines += ["", "| held out of the fit | pointer | lens | n / k / t |", "|---|---|---|---|"]
        lines += [f"| {CUT_WORDS[cut]} | {pct(x['pointer']['ci'])} | {pct(x['lens']['ci'])} | {nkt(x['pointer'])} |"
                  for cut, x in d["per_cut"].items()]  # fmt: skip
        lines += ["", "Overshoot (off-target statement answers beyond the target vs a uniform choice): "
                  + "; ".join(f"{t} {o['beyond']}/{o['n_off_target']} vs {o['expected_uniform']} ({pts(o['beyond_minus_uniform'])} per answer)"
                              for t, o in d["overshoot"].items()),
                  "Shuffled-label direction: " + "; ".join(f"{t} {o['beyond']}/{o['n_off_target']} vs {o['expected_uniform']}"
                                                           for t, o in d["overshoot_shuffled"].items()), ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def summary_md_transit(tr: dict) -> str:
    lines = ["## The transit sweep: C2's kill test, with \"in transit\" defined before the test", "",
             "Lens / random = answers that become bridge alt's answer (memory → prompt: its statement digit; memory → "
             "memory: its recalled fact); copy = memory → prompt answers changed by pasting the alt prompt's states. In "
             "transit: memory → memory lens upper bound <= 2x the random's upper bound, and copy >= 50%.", ""]  # fmt: skip
    for s, d in tr["by_scale"].items():
        lines += [f"### {s}x the alt-prompt patch's size{' (primary)' if float(s) == tr['primary_scale'] else ''}", "",
                  f"Flags: {json.dumps(d['flags'])}", ""]  # fmt: skip
        for t, x in d["topics"].items():
            lines += [f"**{t}**: transit layers {x['transit_layers'] or 'none'}; C2 **{x['c2']}**", "",
                      "| layer | memory → memory lens | memory → memory random | memory → prompt copy (changed) | "
                      "memory → prompt lens | memory → prompt random | lens − random | in transit | C2 |",
                      "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
            lines += [f"| {r['layer']} | {pct(r['rr_lens']['ci'])} | {pct(r['rr_random']['ci'])} | "
                      f"{pct(r['rl_copy_changed']['ci'])} | {pct(r['rl_lens']['ci'])} | {pct(r['rl_random']['ci'])} | "
                      f"{pts(r['rl_lens_minus_random'])} | {r['transit']} | {r['c2'] or '-'} |" for r in x["layers"]]  # fmt: skip
            lines.append("")
    return "\n".join(lines) + "\n"


def summary_md(sm: dict) -> str:
    tr = summary_md_transit(sm["transit"]) if "transit" in sm else ""
    if "v4" in sm:
        return summary_md_v4(sm["v4"]) + tr
    return summary_md_v1(sm) + tr


def summary_md_v1(sm: dict) -> str:
    def r(x):
        b = x["entity_boot"]
        return f"{100 * b[0]:.0f}% [{100 * b[1]:.0f}, {100 * b[2]:.0f}] (n={x['n']}, k={x['k_entities']})"

    lines = [f"# {EXP}", ""]
    for group, d in sm["decisions"].items():
        where = "after the cue" if group == "after" else "question words"
        lines += [f"## memory → prompt, {where}, layers 32-40 at once, 1x: **{d['verdict']}**", "",
                  f"pointer {r(d['pointer'])}; lens {r(d['lens'])}; random {r(d['random'])}; shuffled {r(d['shuffled'])}; "
                  f"patch {r(d['patch'])}", f"memory → memory answers changed by the pointer: {r(d['memory_memory_changed'])}",
                  f"pointer - lens {d['pointer_minus_lens']}; pointer - random {d['pointer_minus_random']}",
                  f"overshoot: {json.dumps(d['overshoot'])}; shuffled: {json.dumps(d['overshoot_shuffled'])}", ""]  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_analyze(name: str) -> Path:
    m = json.loads((RESULTS / name / "manifest.json").read_text())
    sm = summarise(load_rows(name), m["config"])
    out = RESULTS / name / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    (out / "summary.json").write_text(json.dumps(sm, indent=2) + "\n")
    (out / "summary.md").write_text(summary_md(sm))
    print(out)
    return out


# ---- figures and examples ---------------------------------------------------------------------------------------------

COND_STYLE = {"pointer": ("#2a78d6", "-", "pointer push (bridge alt's statement − the asked one)"),
              "lens": ("#eb6834", "-", "lens push (bridge alt − bridge org)"),
              "random": ("#898781", "--", "control: random push (same size)"),
              "shuffled": ("#898781", ":", "control: shuffled-label direction")}  # fmt: skip


def stage_figures(name: str) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace import plotting as PL

    d = RESULTS / name
    m = json.loads((d / "manifest.json").read_text())
    cfg = m["config"]
    for old in d.glob("analysis-*-figures"):
        for f_ in old.iterdir():
            f_.unlink()
        old.rmdir()
    out = d / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    rows = load_rows(name)
    cases = [json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines()]
    sm = summarise(rows, cfg)
    model_name = m["model"]["repo"].split("/")[-1]
    figs: list[str] = []
    if is_v4(cfg) or "pointer" not in arms_of(cfg):
        if "pointer" in arms_of(cfg):
            figures_v4(rows, cases, cfg, sm["v4"], model_name, out, figs)
        if "transit" in sm:
            figure_transit(cases, cfg, sm["transit"], model_name, out, figs)
        keep = {k: sm[k] for k in ("v4", "transit") if k in sm}
        (out / "summary.json").write_text(json.dumps({"run": name, **keep, "figures": figs}, indent=2) + "\n")
        print(out)
        return out
    rl = next((c for c in cases if c["family"] == "RL"), None)
    ex = ""
    if rl:
        q = rl["text"][rl["text"].rindex("Which") :].split("?")[0] + "?"
        ex = (f"\"... {rl['context'][:80]}... {q}\" -> answer org {rl['answer']} (bridge org {rl['query']}); both pushes "
              f"aim at {rl['target_digit']}, the digit of bridge alt's statement ({rl['alt_query']}).")  # fmt: skip
    win = window_key(cfg["layers"])
    keys = [*cfg["layers"], win]
    xs = np.arange(len(keys))
    panels = [(fam, grp) for fam, grp in (("RL", "after"), ("RL", "question"), ("DL", "after"), ("BL", "after"))
              if sel(rows, family=fam, group=grp)]  # fmt: skip
    fig, axes = plt.subplots(len(panels), len(cfg["scales"]), figsize=(3.9 * len(cfg["scales"]), 3.1 * len(panels) + 0.4),
                             squeeze=False, sharey=True)  # fmt: skip
    for i, (fam, grp) in enumerate(panels):
        for jx, sc in enumerate(cfg["scales"]):
            ax = axes[i][jx]
            PL.style_axes(ax)
            PL.percent_axis(ax)
            for k_, cn in enumerate(CONDS):
                colour, ls, _ = COND_STYLE[cn]
                v = np.array([stat(sel(rows, family=fam, group=grp, layer=key, scale=sc, cond=cn))["entity_boot"]
                              if sel(rows, family=fam, group=grp, layer=key, scale=sc, cond=cn) else [math.nan] * 3 for key in keys], float)  # fmt: skip
                ax.errorbar(xs + (k_ - 1.5) * 0.08, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None),
                            color=colour, ls=ls, lw=2 if cn in ("pointer", "lens") else 1.2, marker="o", ms=4,
                            mfc=colour if cn in ("pointer", "lens") else PL.SURFACE, elinewidth=1, capsize=0)  # fmt: skip
            ax.set_xticks(xs, [str(k) if k != win else f"all {len(cfg['layers'])}" for k in keys])
            ax.set_ylim(-0.04, 1.04)
            if i == 0:
                ax.set_title(f"{sc:g}x the alt-prompt patch's size", fontsize=9.5, color=PL.INK, loc="left")
            if jx == 0:
                where = (
                    ("after the subject" if fam == "BL" else "after the cue") if grp == "after" else "question words"
                )
                ax.set_ylabel(
                    f"{FAMILY_WORDS[fam]}, {where}\n% of original answers that become\nbridge alt's statement digit",
                    fontsize=8,
                    color=PL.INK,
                )
            if i == len(panels) - 1:
                ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
    handles = [Line2D([], [], color=c_, ls=ls, lw=2, marker="o", label=lab) for c_, ls, lab in COND_STYLE.values()]
    dec = sm["decisions"].get("after", {})
    explain = [("What we did", "At layers 32-40, where the lens reads the recalled word, pushed the tokens after the cue "
                               "(and the question words) along a fitted pointer to bridge alt's statement, or along the lens "
                               "direction bridge alt − bridge org, at the same size; both aim at the same digit."),
               ("Example", ex),
               ("How to read", f"Each dot: share of answers that become bridge alt's statement digit. Deciding cell "
                               f"(memory → prompt, after the cue, all 3 layers, 1x): '{dec.get('verdict', '-')}'."),
               ("Control", "Gray: a random push and a shuffled-label direction of the same size. Memory → memory items "
                           "(nothing looked up; must stay under 10%): the pointer push changed "
                           + (f"{100 * dec['memory_memory_changed']['entity_boot'][0]:.0f}% "
                              f"[{100 * dec['memory_memory_changed']['entity_boot'][1]:.0f}, "
                              f"{100 * dec['memory_memory_changed']['entity_boot'][2]:.0f}]" if dec else "-")
                           + " of their answers.")]  # fmt: skip
    PF.save_fig(fig, out, "fig1_pointer_vs_lens_32_40", "Where the lens reads the word, does a pointer code steer the lookup when the lens push cannot?",
                explain, f"{model_name}; held-out scenes; error bars: bootstrap over the asked entities within each topic.",
                handles, ncols=2, figs=figs)  # fmt: skip
    if "transit" in sm:
        figure_transit(cases, cfg, sm["transit"], model_name, out, figs)
    (out / "summary.json").write_text(
        json.dumps({"run": name, "decisions": sm["decisions"], "figures": figs}, indent=2) + "\n"
    )
    print(out)
    return out


TOPIC_WORDS = {"countries": "countries", "animals": "animals", "body": "body parts", "elements": "elements",
               "pooled": "all topics"}  # fmt: skip


def example_text(cases: list[dict], aim: str = "both pushes aim at") -> str:
    c = next((x for x in cases if x["family"] == "RL"), None)
    if c is None:
        return ""
    sents = re.split(r"(?<=\.) ", c["context"])
    return (f"\"{sents[c['asked']]} ... {sents[c['target_slot']]} ... {c['question']}\" -> answer org {c['answer']} "
            f"(bridge org {c['query']}, recalled from the cue); {aim} {c['target_digit']}, the digit of "
            f"bridge alt's statement ({c['alt_query']}).")  # fmt: skip


def figures_v4(rows: list[dict], cases: list[dict], cfg: dict, v4: dict, model_name: str, out: Path,
               figs: list[str]) -> None:  # fmt: skip
    """pointer_v4: (1) the deciding cell per topic with the memory → memory control, (2) after the cue by layer and
    size per topic, (3) the question words by layer and size per topic."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace import plotting as PL

    sc, win, topics = cfg["primary_scale"], v4["window"], list(cfg["domains"])
    ex = example_text(cases)
    flip_label = "% of original answers that become\nbridge alt's statement digit"
    data = (f"{model_name}; memory → prompt and memory → memory items whose asked entity or wording the fit never saw; "
            "error bars: bootstrap over the asked entities within each topic (95%), widened to the item-level interval "
            "where that is wider.")  # fmt: skip
    after = v4.get("after", {})
    tp = after.get("topics", {})
    # (1) the deciding cell per topic
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 7.4))
    keys = [*topics, "pooled"]
    xs = np.arange(len(keys))
    for ax, metric, ylab, line in ((axes[0], "target", flip_label, RATE_MIN),
                                   (axes[1], "rr", "% of original answers changed", CONTROL_MAX)):  # fmt: skip
        PL.style_axes(ax)
        PL.percent_axis(ax)
        for k_, cn in enumerate(CONDS):
            colour, _, _ = COND_STYLE[cn]
            v = np.array([(tp[t][cn]["ci"] if metric == "target" else tp[t]["memory_memory_changed_by"][cn]["ci"])
                          if t in tp else [math.nan] * 3 for t in keys], float)  # fmt: skip
            ax.bar(xs + (k_ - 1.5) * 0.19, v[:, 0], 0.18, color=colour if cn in ("pointer", "lens") else PL.SURFACE,
                   edgecolor=colour, hatch="//" if cn == "shuffled" else None, linewidth=1)  # fmt: skip
            ax.errorbar(xs + (k_ - 1.5) * 0.19, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None),
                        fmt="none", ecolor=PL.INK, elinewidth=0.9)  # fmt: skip
        ax.axhline(line, color=PL.INK, ls=":", lw=1)
        ax.text(-0.45, line + 0.015, f"{100 * line:.0f}%", fontsize=8, color=PL.INK, ha="left", va="bottom")
        ax.set_xticks(xs, [TOPIC_WORDS.get(t, t) for t in keys])
        ax.set_ylim(0, 1.0)
        ax.set_ylabel(ylab, fontsize=8.5, color=PL.INK)
    axes[0].set_title("memory → prompt (the lookup)", fontsize=9.5, color=PL.INK, loc="left")
    axes[1].set_title("memory → memory (nothing looked up)", fontsize=9.5, color=PL.INK, loc="left")
    handles = [Patch(facecolor=COND_STYLE[cn][0] if cn in ("pointer", "lens") else PL.SURFACE,
                     edgecolor=COND_STYLE[cn][0], hatch="//" if cn == "shuffled" else None, label=COND_STYLE[cn][2])
               for cn in CONDS]  # fmt: skip
    passing = ", ".join(TOPIC_WORDS[t] for t in topics if t in tp and tp[t]["passes"] and tp[t]["valid"]) or "none"
    explain = [("What we did", f"At layers {win} at once, where the lens reads the recalled word, pushed the tokens "
                               f"after the cue along a fitted pointer to bridge alt's statement, or along the lens "
                               f"direction bridge alt − bridge org, at {sc:g}x the alt-prompt patch's size; both aim at the "
                               "same digit."),
               ("Example", ex),
               ("How to read", "Left: share of lookups whose answer becomes bridge alt's statement digit. A topic passes if "
                               "the pointer's interval stays above 30% and 20 points above the lens push and the random "
                               "push; the claim needs 2 of 3 topics. Right: the same pushes on questions with nothing to "
                               f"look up, where a pointer should change nothing. Verdict: '{after.get('verdict', '-')}' "
                               f"(passing topics: {passing})."),
               ("Control", "Gray: a random push and a shuffled-label direction of the same size; right: memory → "
                           "memory answers must stay under 10% changed.")]  # fmt: skip
    PF.save_fig(fig, out, "fig1_deciding_cell_by_topic", "Where the lens reads the word, does a pointer push steer the "
                "lookup when the lens push cannot? Per topic", explain, data, handles, ncols=2, figs=figs)  # fmt: skip
    # (2), (3) by layer and size, per topic
    lkeys = [*cfg["layers"], win]
    lx = np.arange(len(lkeys))
    for stem, group, where in (("fig2_after_cue_by_layer", "after", "after the cue"),
                               ("fig3_question_words_by_layer", "question", "at the question words")):  # fmt: skip
        if not sel(rows, family="RL", group=group):
            continue
        fig, axes = plt.subplots(len(topics), len(cfg["scales"]), figsize=(3.9 * len(cfg["scales"]) + 0.6, 2.6 * len(topics) + 5.0),
                                 squeeze=False, sharey=True)  # fmt: skip
        for i, t in enumerate(topics):
            for jx, s in enumerate(cfg["scales"]):
                ax = axes[i][jx]
                PL.style_axes(ax)
                PL.percent_axis(ax)
                for k_, cn in enumerate(CONDS):
                    colour, ls, _ = COND_STYLE[cn]
                    cells = [
                        sel(rows, family="RL", group=group, layer=key, scale=s, cond=cn, domain=t) for key in lkeys
                    ]
                    v = np.array([stat(c_)["ci"] if c_ else [math.nan] * 3 for c_ in cells], float)
                    ax.errorbar(lx + (k_ - 1.5) * 0.08, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None),
                                color=colour, ls=ls, lw=2 if cn in ("pointer", "lens") else 1.2, marker="o", ms=4,
                                mfc=colour if cn in ("pointer", "lens") else PL.SURFACE, elinewidth=1, capsize=0)  # fmt: skip
                ax.set_xticks(lx, [str(k) if k != win else f"all {len(cfg['layers'])}" for k in lkeys])
                ax.set_ylim(-0.04, 1.04)
                if i == 0:
                    ax.set_title(f"{s:g}x the alt-prompt patch's size", fontsize=9.5, color=PL.INK, loc="left")
                ax.text(0.02, 0.97, TOPIC_WORDS.get(t, t), transform=ax.transAxes, fontsize=9, color=PL.INK,
                        fontweight="bold", va="top")  # fmt: skip
                if jx == 0 and i == len(topics) // 2:
                    ax.set_ylabel(flip_label, fontsize=8.5, color=PL.INK)
                if i == len(topics) - 1:
                    ax.set_xlabel("layer pushed", fontsize=9, color=PL.MUTED)
        handles = [Line2D([], [], color=c_, ls=ls, lw=2, marker="o", label=lab) for c_, ls, lab in COND_STYLE.values()]
        how = ("Each dot: share of memory → prompt answers that become bridge alt's statement digit, per topic, per "
               "layer pushed and size." + (" The pointer here is one direction per statement (the mean over the "
                                           "question's words, whose number differs between wordings): reported, not "
                                           "decisive." if group == "question" else ""))  # fmt: skip
        rr_txt = "; ".join(f"{TOPIC_WORDS.get(t, t)} {pct(v4[group]['topics'][t]['memory_memory_changed']['ci'])}"
                           for t in topics if group in v4 and t in v4[group]["topics"])  # fmt: skip
        explain = [("What we did", f"Pushed the tokens {where} along the fitted pointer to bridge alt's statement or "
                                   "along the lens direction bridge alt − bridge org, at the same size, at one layer or "
                                   "all at once; both aim at the same digit."),
                   ("Example", ex), ("How to read", how),
                   ("Control", "Gray: a random push and a shuffled-label direction of the same size. Memory → memory "
                               f"answers changed by the pointer push ({win}, {sc:g}x): {rr_txt}.")]  # fmt: skip
        PF.save_fig(fig, out, stem, f"Pointer push vs lens push {where}, by layer, size and topic", explain, data,
                    handles, ncols=2, figs=figs)  # fmt: skip


TRANSIT_STYLE = {  # key: (family, condition, colour, line style, filled, label)
    "rl_lens": ("#eb6834", "-", True, "memory → prompt: lens push, % that become bridge alt's statement digit"),
    "rl_random": ("#898781", "--", False, "memory → prompt: random push of the same size, the same %"),
    "rl_copy_changed": ("#1baf7a", "-", True, "memory → prompt: alt-prompt copy, % of answers changed"),
    "rr_lens": ("#eb6834", ":", False, "memory → memory: lens push, % that become bridge alt's recalled fact"),
    "rr_random": ("#898781", ":", False, "memory → memory: random push of the same size, the same %"),
}  # fmt: skip


def figure_transit(cases: list[dict], cfg: dict, tr: dict, model_name: str, out: Path, figs: list[str]) -> None:
    """The transit sweep: per topic (rows) and size (columns), the lens and random push on both families and the
    alt-prompt copy by layer; the layers in transit shaded."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    from bridge_jspace import plotting as PL

    topics, scales = list(cfg["domains"]), [f"{s:g}" for s in cfg["transit_scales"]]
    lay = list(cfg["transit_layers"])
    fig, axes = plt.subplots(len(topics), len(scales), figsize=(4.6 * len(scales) + 0.6, 2.6 * len(topics) + 5.4),
                             squeeze=False, sharey=True)  # fmt: skip
    for i, t in enumerate(topics):
        for jx, s in enumerate(scales):
            ax = axes[i][jx]
            PL.style_axes(ax)
            PL.percent_axis(ax)
            x = tr["by_scale"][s]["topics"][t]
            for la in x["transit_layers"]:
                ax.axvspan(la - 1.6, la + 1.6, color="#1baf7a", alpha=0.10, lw=0)
            for key, (colour, ls, filled, _) in TRANSIT_STYLE.items():
                v = np.array([r[key]["ci"] for r in x["layers"]], float)
                ax.errorbar(lay, v[:, 0], yerr=np.clip([v[:, 0] - v[:, 1], v[:, 2] - v[:, 0]], 0, None), color=colour,
                            ls=ls, lw=1.8 if filled else 1.2, marker="o", ms=3.5, mfc=colour if filled else PL.SURFACE,
                            elinewidth=0.8, capsize=0)  # fmt: skip
            ax.set_xticks(lay, [str(la) for la in lay])
            ax.set_ylim(-0.04, 1.04)
            ax.text(0.02, 0.97, f"{TOPIC_WORDS.get(t, t)}: C2 {x['c2']}", transform=ax.transAxes, fontsize=9,
                    color=PL.INK, fontweight="bold", va="top")  # fmt: skip
            if i == 0:
                ax.set_title(
                    f"{s}x the alt-prompt patch's size (lens and random push)", fontsize=9.5, color=PL.INK, loc="left"
                )
            if jx == 0 and i == len(topics) // 2:
                ax.set_ylabel("% of original answers (see legend)", fontsize=8.5, color=PL.INK)
            if i == len(topics) - 1:
                ax.set_xlabel("layer pushed (tokens after the cue)", fontsize=9, color=PL.MUTED)
    handles: list[Any] = [Line2D([], [], color=c_, ls=ls, lw=1.8, marker="o", mfc=c_ if f_ else PL.SURFACE, label=lab)
                          for c_, ls, f_, lab in TRANSIT_STYLE.values()]  # fmt: skip
    handles.append(Patch(facecolor="#1baf7a", alpha=0.25, label="in transit (defined before the test)"))
    prim = tr["by_scale"][f"{tr['primary_scale']:g}"]
    verdicts = "; ".join(f"{TOPIC_WORDS.get(t, t)}: {prim['topics'][t]['c2']} (transit layers "
                         f"{', '.join(map(str, prim['topics'][t]['transit_layers'])) or 'none'})" for t in topics)  # fmt: skip
    explain = [("What we did", "Pushed the tokens after the cue at one layer at a time along the lens direction "
                               "bridge alt − bridge org (or a random direction of the same size), on lookups of a recalled "
                               "word (memory → prompt) and on recall questions (memory → memory); and pasted the alt "
                               "prompt's states there (alt-prompt copy)."),
               ("Example", example_text(cases, "the lens push aims at")),
               ("How to read", "Shaded: layers in transit for that topic: the lens push no longer changes the recalled "
                               "fact (memory → memory, orange dotted, at most 2x the random push) while pasting the alt "
                               "prompt still changes at least half of the lookups (green). C2 holds there if the lens push "
                               "on lookups (orange solid) stays under 3x the random push or under 10%. "
                               f"At {tr['primary_scale']:g}x: {verdicts}."),
               ("Control", "Gray: a random push of the same size on each family.")]  # fmt: skip
    PF.save_fig(fig, out, "fig4_transit_sweep", "Where the recalled word is in transit, can the lens push write the "
                "lookup? (C2's kill test)", explain, f"{model_name}; error bars: bootstrap over the asked entities within "
                "each topic (95%), widened to the item-level interval where that is wider.", handles, ncols=1, figs=figs)  # fmt: skip


def examples_transit(name: str, path: Path, cfg: dict, rows: list[dict], cases: dict[str, dict], k: int,
                     seed: int) -> None:  # fmt: skip
    """A transit-only run: memory → prompt items at layer 40 (the kill test's cell; else the middle layer), primary size,
    grouped by what the lens push and the alt-prompt copy do there."""
    lay = list(cfg["transit_layers"])
    la, sc = (40 if 40 in lay else lay[len(lay) // 2]), cfg["primary_scale"]
    cells = {cn: sel(rows, family="RL", group=TRANSIT, layer=la, scale=None if cn == "patch" else sc, cond=cn)
             for cn in ("lens", "random", "patch")}  # fmt: skip
    groups = {"lens_writes": "the lens push gives bridge alt's statement digit",
              "copy_only": "the alt-prompt copy changes the answer, the lens push does not give bridge alt's digit",
              "neither": "neither"}  # fmt: skip
    members: dict[str, list[str]] = {g: [] for g in groups}
    for n, o in cells["lens"].items():
        copy_changed = cells["patch"].get(n, {}).get("changed", False)
        members["lens_writes" if o["role"] == "target" else "copy_only" if copy_changed else "neither"].append(n)
    rng = np.random.default_rng(seed)
    words = {
        "lens": COND_STYLE["lens"][2],
        "random": COND_STYLE["random"][2],
        "patch": "alt-prompt copy (pasted states)",
    }
    examples = []
    for g, names in members.items():
        for n in (
            [names[i] for i in sorted(rng.choice(len(names), size=min(k, len(names)), replace=False))] if names else []
        ):
            c = cases[n]
            spans = PF.statement_spans(c["text"], c["context"])
            base = [{"start": spans[c["asked"]][0], "end": spans[c["asked"]][1], "role": "asked statement"},
                    {"start": spans[c["target_slot"]][0], "end": spans[c["target_slot"]][1], "role": "bridge alt's statement"},
                    {"start": c["groups_chars"]["after"][0], "end": c["groups_chars"]["after"][1], "role": "pushed tokens"}]  # fmt: skip
            for cn, cell in cells.items():
                o = cell.get(n)
                if o is None:
                    continue
                size = "" if cn == "patch" else f", {sc:g}x the alt-prompt patch's size"
                examples.append({"group": g, "family": "RL", "item_id": n, "prompt": c["text"] + " ", "spans": base,
                                 "condition": f"{words[cn]}, layer {la}{size}",
                                 "answers": {"clean": c["answer"], "edited": o["top"],
                                             "expected": {"C2 holds": c["answer"] if cn == "lens" else "-",
                                                          "lens writes": c["target_digit"] if cn == "lens" else "-"}},
                                 "numbers": {"role": o["role"], "changed": o["changed"], "topic": c["domain"]},
                                 "why": groups[g]})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k, "layer": la,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


def stage_examples(name: str, k: int = 3, seed: int = EXAMPLE_SEED) -> None:
    d = RESULTS / name
    path = d / "examples.json"
    assert not path.exists(), f"{path} exists; written once"
    m = json.loads((d / "manifest.json").read_text())
    sc = m["config"]["primary_scale"]
    win = window_key(m["config"]["layers"])
    rows = load_rows(name)
    cases = {c["id"]: c for c in (json.loads(x) for x in (d / "cases.jsonl").read_text().splitlines())}
    if "pointer" not in arms_of(m["config"]):
        examples_transit(name, path, m["config"], rows, cases, k, seed)
        return
    prim = sel(rows, family="RL", group="after", layer=win, scale=sc, cond="pointer")
    lens_c = sel(rows, family="RL", group="after", layer=win, scale=sc, cond="lens")
    groups = {"pointer_only": "the pointer push gives bridge alt's digit, the lens push does not",
              "both": "both give it", "neither": "neither gives it", "lens_only": "only the lens push gives it"}  # fmt: skip
    members: dict[str, list[str]] = {g: [] for g in groups}
    for n, o in prim.items():
        p_hit, l_hit = o["role"] == "target", lens_c.get(n, {}).get("role") == "target"
        members["both" if p_hit and l_hit else "pointer_only" if p_hit else "lens_only" if l_hit else "neither"].append(
            n
        )
    rng = np.random.default_rng(seed)
    examples = []
    for g, names in members.items():
        for n in (
            [names[i] for i in sorted(rng.choice(len(names), size=min(k, len(names)), replace=False))] if names else []
        ):
            c = cases[n]
            spans = PF.statement_spans(c["text"], c["context"])
            base = [{"start": spans[c["asked"]][0], "end": spans[c["asked"]][1], "role": "asked statement"},
                    {"start": spans[c["target_slot"]][0], "end": spans[c["target_slot"]][1], "role": "bridge alt's statement"},
                    {"start": c["groups_chars"]["after"][0], "end": c["groups_chars"]["after"][1], "role": "pushed tokens"}]  # fmt: skip
            for cn in ("pointer", "lens", "random", "shuffled"):
                o = sel(rows, name=n, family="RL", group="after", layer=win, scale=sc, cond=cn).get(n)
                if o is None:
                    continue
                examples.append({"group": g, "family": "RL", "item_id": n, "prompt": c["text"] + " ", "spans": base,
                                 "condition": f"{COND_STYLE[cn][2]}, layers {win}, {sc:g}x the alt-prompt patch's size",
                                 "answers": {"clean": c["answer"], "edited": o["top"],
                                             "expected": {"H-pointer": c["target_digit"] if cn == "pointer" else c["answer"],
                                                          "H-lens": c["target_digit"] if cn == "lens" else c["answer"]}},
                                 "numbers": {"role": o["role"], "answer_statement": o["answer_slot"], "topic": c["domain"],
                                             **({"held_out": CUT_WORDS[c["cut"]]} if c.get("cut") in CUT_WORDS else {})},
                                 "why": groups[g]})  # fmt: skip
    blob = {"exp": EXP, "run": name, "seed": seed, "k": k,
            "groups": [{"key": g, "title": g.replace("_", " "), "definition": t, "n_total": len(members[g])} for g, t in groups.items()],
            "examples": examples}  # fmt: skip
    path.write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze", "figures", "examples"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--data", choices=["pointer_v1", "pointer_v4"], default=DEFAULTS["data"])
    ap.add_argument(
        "--domains", nargs="+", default=None, help="default: pointer_v1 animals elements; pointer_v4 all used"
    )
    ap.add_argument("--layers", nargs="+", type=int, default=DEFAULTS["layers"])
    ap.add_argument("--scales", nargs="+", type=float, default=None, help="default: 0.5 1 2 4; pointer_v4: 1 2")
    ap.add_argument(
        "--n",
        nargs=4,
        type=int,
        metavar=("RL", "DL", "RR", "BL"),
        default=None,
        help="items per topic for memory → prompt, named → prompt, memory → memory; scenes for prompt → prompt "
        "(pointer_v4 default: 250 0 250 0, i.e. every held-out eligible item, no named → prompt, no suite)",
    )
    ap.add_argument("--competence", default=None, help=f"default: {DEFAULTS['competence']}; pointer_v4: required")
    ap.add_argument("--no-eligibility", action="store_true", help="a smoke on another model: no competence filter")
    ap.add_argument("--keep-wrong", action="store_true", help="a smoke on a weak model: fit on wrong answers too")
    ap.add_argument("--no-suite", action="store_true", help="skip the animal suite's prompt → prompt items")
    ap.add_argument("--fit-limit", type=int, default=None)
    ap.add_argument(
        "--arms", nargs="+", choices=ARMS, default=None, help="default: pointer; pointer_v4: pointer transit"
    )
    ap.add_argument("--transit-layers", nargs="+", type=int, default=DEFAULTS["transit_layers"])
    ap.add_argument("--transit-scales", nargs="+", type=float, default=DEFAULTS["transit_scales"])
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        v4 = args.data == "pointer_v4"
        base = {**DEFAULTS, **(V4_DEFAULTS if v4 else {})}
        competence = args.competence or (None if v4 else DEFAULTS["competence"])
        assert competence or args.no_eligibility, "pointer_v4 needs --competence RUN (or --no-eligibility for a smoke)"
        n = dict(zip(("RL", "DL", "RR", "BL"), args.n, strict=True)) if args.n else base["n"]
        domains = args.domains or (list(PF.data_gen({"data": args.data}).DOMAINS) if v4 else DEFAULTS["domains"])
        stage_run(args.name, args.why, {"data": args.data, "domains": domains, "layers": args.layers,
                                        "scales": args.scales or base["scales"], "n": n,
                                        "competence": None if args.no_eligibility else competence,
                                        "suite": base["suite"] and not args.no_suite,
                                        "primary_scale": DEFAULTS["primary_scale"], "fit_limit": args.fit_limit,
                                        "require_correct": not args.keep_wrong, "arms": args.arms or base["arms"],
                                        "transit_layers": args.transit_layers, "transit_scales": args.transit_scales})  # fmt: skip
    elif args.stage == "analyze":
        stage_analyze(args.name)
    elif args.stage == "figures":
        stage_figures(args.name)
    else:
        stage_examples(args.name, args.k)
