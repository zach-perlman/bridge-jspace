"""x0_necessity (X0, jobs/c3/X0.md): is C3's split real at a layer fixed in advance, and is it about the J++-space?

At the bridge's word and layer L, Δ = h_alt - h_org (one row). Arms on the org run: whole (Δ), and per dictionary D
(J++, W_U, W_E, random; k-atom OMP over the target's letter-token atoms) no_part (Δ - D(Δ)) and no_rand (Δ minus a
random subspace's part of D(Δ)'s share). A lookup (PP) and a recall (PM) read the identical patched context. Switch =
the alt answer's first token ranks first among the digit tokens (the relation's candidates on these sets).

Per cell (rendering, layer, reader, dictionary, k): S_x = share switched by arm x; Jdep = 1 - S_no_part / S_whole;
Rdep = 1 - S_no_rand / S_whole; excess = Jdep - Rdep; 95% percentile CIs from a cluster bootstrap over the org bridge
entity (10,000 resamples, seed 0). Valid iff S_whole >= 0.30 and >= 30 items switched by the whole edit. Labels:
around (excess <= 0.10, upper bound <= 0.20), through (Jdep >= 0.30, excess >= 0.20, lower bound >= 0.10), else mixed.
Rule (23 Oct, at the predicted layer, chat rendering, J++): confirmed iff lookup excess <= 0.10 and recall Jdep >=
0.30; killed iff lookup excess >= 0.20 or recall Jdep < 0.20; else not confirmed; can't tell if either cell is invalid.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.stats import wilson

EXP = "x0_necessity"
DICTS = ("jpp", "wu", "we", "rand")  # J++ (main arm), the logit lens's W_U, the input embeddings W_E, Gaussian
K_MAIN = 25
K_CURVE = (10, 50, 100)  # at the predicted layer only, for CURVE_DICTS
CURVE_DICTS = ("jpp", "we")
ARMS = ("whole", "no_part", "no_rand")
READERS = ("PP", "PM")  # lookup, recall
LOOKUP, RECALL = READERS
RAND_DICT_SEED, SUBSPACE_SEED = 777, 888  # + layer, as on 23 Oct
BOOT_SEED, N_BOOT = 0, 10_000
VALID_S, VALID_N = 0.30, 30
AROUND_EXCESS, AROUND_HI = 0.10, 0.20
THROUGH_JDEP, THROUGH_EXCESS, THROUGH_LO = 0.30, 0.20, 0.10
CONFIRM_LOOKUP_EXCESS, CONFIRM_RECALL_JDEP = 0.10, 0.30
KILL_LOOKUP_EXCESS, KILL_RECALL_JDEP = 0.20, 0.20
H_TOKEN_EXCESS = 0.20
PREDICTED = {"qwen3.6-27b": 32, "qwen3.5-9b": 12, "qwen3.5-122b-a10b": 33}


# ---- cells (CPU) --------------------------------------------------------------------------------------------------


def resampled_rates(
    switched: dict[str, list[int]], entities: list[str], n_boot: int = N_BOOT, seed: int = BOOT_SEED
) -> dict[str, np.ndarray]:
    """Per arm, the switched share in each cluster-bootstrap resample [n_boot]: whole entities drawn with replacement,
    the same draws for every arm (so ratios of arms are paired)."""
    keys = sorted(set(entities))
    index = {e: i for i, e in enumerate(keys)}
    ent = np.array([index[e] for e in entities])
    counts = np.bincount(ent, minlength=len(keys)).astype(float)
    pick = np.random.default_rng(seed).integers(0, len(keys), size=(n_boot, len(keys)))
    n_r = counts[pick].sum(1)
    out = {}
    for arm, s in switched.items():
        assert len(s) == len(entities), f"{arm}: {len(s)} outcomes for {len(entities)} items"
        sums = np.bincount(ent, weights=np.asarray(s, dtype=float), minlength=len(keys))
        out[arm] = sums[pick].sum(1) / n_r
    return out


def dependence(s_whole: float | np.ndarray, s_removed: float | np.ndarray) -> np.ndarray:
    """1 - S_removed / S_whole (nan where nothing switched with the whole edit); a 0-d array for scalars."""
    whole = np.asarray(s_whole, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return 1.0 - np.asarray(s_removed, dtype=float) / np.where(whole > 0, whole, np.nan)


def interval(x: np.ndarray) -> tuple[float, float]:
    lo, hi = np.nanpercentile(x, [2.5, 97.5])
    return float(lo), float(hi)


def cell(switched: dict[str, list[int]], entities: list[str], n_boot: int = N_BOOT, seed: int = BOOT_SEED) -> dict:
    """One cell's numbers from per-item 0/1 outcomes of the three arms (whole, no_part, no_rand), with its label."""
    assert set(switched) == set(ARMS), f"arms {sorted(switched)}"
    n = len(entities)
    hits = {a: int(sum(switched[a])) for a in ARMS}
    s = {a: hits[a] / n for a in ARMS}
    r = resampled_rates(switched, entities, n_boot, seed)
    jdep_r, rdep_r = dependence(r["whole"], r["no_part"]), dependence(r["whole"], r["no_rand"])
    jdep, rdep = float(dependence(s["whole"], s["no_part"])), float(dependence(s["whole"], s["no_rand"]))
    out = {
        "n": n,
        "entities": len(set(entities)),
        **{f"S_{a}": [round(v, 4) for v in wilson(hits[a], n)] for a in ARMS},
        "switched_whole": hits["whole"],
        "valid": s["whole"] >= VALID_S and hits["whole"] >= VALID_N,
        "Jdep": [jdep, *interval(jdep_r)],
        "Rdep": [rdep, *interval(rdep_r)],
        "excess": [jdep - rdep, *interval(jdep_r - rdep_r)],
    }
    out["label"] = label(out)
    return out


def label(c: dict) -> str:
    """around / through / mixed (section 2 of the brief); can't tell for an invalid cell."""
    if not c["valid"]:
        return "can't tell"
    ex, ex_lo, ex_hi = c["excess"]
    if ex <= AROUND_EXCESS and ex_hi <= AROUND_HI:
        return "around"
    if c["Jdep"][0] >= THROUGH_JDEP and ex >= THROUGH_EXCESS and ex_lo >= THROUGH_LO:
        return "through"
    return "mixed"


def verdict(lookup: dict, recall: dict) -> str:
    """The 23 Oct rule at the predicted layer (point estimates): confirmed / killed / not confirmed / can't tell."""
    if not (lookup["valid"] and recall["valid"]):
        return "can't tell"
    lk_excess, rc_jdep = lookup["excess"][0], recall["Jdep"][0]
    if lk_excess <= CONFIRM_LOOKUP_EXCESS and rc_jdep >= CONFIRM_RECALL_JDEP:
        return "confirmed"
    if lk_excess >= KILL_LOOKUP_EXCESS or rc_jdep < KILL_RECALL_JDEP:
        return "killed"
    return "not confirmed"


def h_token(jpp_lookup: dict, we_lookup: dict) -> str:
    """H-token at the predicted layer: does W_E removal make the lookup need its part while J++ removal leaves it
    around?"""
    if not (jpp_lookup["valid"] and we_lookup["valid"]):
        return "can't tell"
    if jpp_lookup["label"] != "around":
        return "not applicable (the J++ lookup is not around)"
    if we_lookup["excess"][0] >= H_TOKEN_EXCESS:
        return "token identity: W_E removal costs the lookup, J++ removal does not"
    if we_lookup["label"] == "around":
        return "neither: the lookup is around W_E as well as J++"
    return "mixed"


def split(lookup: dict, recall: dict) -> bool:
    """The split at a layer: the lookup around and the recall through, on the same items."""
    return lookup["label"] == "around" and recall["label"] == "through"


def nan_round(x: float, nd: int = 3) -> float | None:
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(x, nd)
