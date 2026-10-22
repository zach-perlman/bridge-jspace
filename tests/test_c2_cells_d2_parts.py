"""The step-a cell selection (scripts/c2_cells.py) and the name / digit verdicts (scripts/d2_parts.py) on synthetic rows."""

from __future__ import annotations

from scripts import c2_cells as C
from scripts import d2_parts as P


def _rows(family: str, domain: str, layer: int, cond: str, scale: float | None, hits: int, n: int, names: list[str]):
    return [{"family": family, "domain": domain, "layer": layer, "cond": cond, "scale": scale,
             "role": "identity" if i < hits else "none", "name": names[i % len(names)]} for i in range(n)]  # fmt: skip


def _cases(names: list[str], target_slot: int) -> dict[str, dict]:
    return {n: {"query": f"e{i}", "target_slot": target_slot} for i, n in enumerate(names)}


def test_select_needs_lens_on_recall_a_quiet_random_and_a_working_patch():
    names = [f"rr{i}" for i in range(40)]
    cases = _cases(names, 2)
    good = (_rows("RR", "elements", 44, "lens", 1.0, 14, 40, names) + _rows("RR", "elements", 44, "lens", 2.0, 4, 40, names)
            + _rows("RR", "elements", 44, "random", 1.0, 0, 40, names)
            + _rows("RR", "elements", 44, "random", 2.0, 1, 40, names)
            + _rows("RR", "elements", 44, "patch", None, 12, 40, names))  # fmt: skip
    noisy = [{**r, "layer": 46} for r in good] + _rows("RR", "elements", 46, "random", 2.0, 5, 40, names)
    noisy = [r for r in noisy if not (r["cond"] == "random" and r["scale"] == 2.0 and r["role"] == "none")] + [
        {**r, "role": "none"} for r in _rows("RR", "elements", 46, "random", 2.0, 0, 35, names)
    ]
    cells = {c["layer"]: c for c in C.select_cells("run", cases, good + noisy)}
    assert cells[44]["selected"] and cells[44]["lens_size"] == 1.0
    assert not cells[46]["selected"]  # the random push moves 5 of 40 recalls (> 0.05)
    # the reveal: lookups of statements 3-5 in the selected cell, at the size that wrote recall (1x)
    rl_names = [f"rl{i}" for i in range(60)]
    rl_cases = {**cases, **_cases(rl_names, 3)}
    rl = (_rows("RL", "elements", 44, "patch", None, 18, 60, rl_names)
          + _rows("RL", "elements", 44, "lens", 1.0, 0, 60, rl_names)
          + _rows("RL", "elements", 44, "random", 1.0, 0, 60, rl_names))  # fmt: skip
    parts = C.cell_rows(cells[44], rl_cases, good + rl)
    assert len(parts["patch"]) == 60 and len(parts["rr_lens"]) == 40
    j = C.judge(parts, rl_cases, cluster=False)
    assert j["state"] == "holds" and len(j["entities"]) == 60  # lens 0 of 60 (upper bound ~6%) vs recall lower ~22%
    ident = _rows("RL", "elements", 44, "ident", 1.0, 12, 60, rl_names) + _rows(
        "RR", "elements", 44, "ident", 1.0, 10, 40, names
    )
    assert C.judge(C.cell_rows(cells[44], rl_cases, good + rl + ident), rl_cases, cluster=False)["two_codes"]
    weak_rr = ident[:60] + _rows("RR", "elements", 44, "ident", 1.0, 4, 40, names)  # recall 10%: not a bridge code
    assert not C.judge(C.cell_rows(cells[44], rl_cases, good + rl + weak_rr), rl_cases, cluster=False)["two_codes"]


def test_c2_states():
    assert C.c2_state(patch=0.10, lens=0.0, lens_hi=0.05, rand=0.0, recall_lo=0.3) == "not testable"
    assert C.c2_state(patch=0.30, lens=0.20, lens_hi=0.30, rand=0.02, recall_lo=0.3) == "refuted"
    assert C.c2_state(patch=0.30, lens=0.02, lens_hi=0.10, rand=0.0, recall_lo=0.25) == "holds"
    assert C.c2_state(patch=0.30, lens=0.02, lens_hi=0.15, rand=0.0, recall_lo=0.25) == "inconclusive"  # 0.15 > 0.125


def test_primary_takes_one_layer_per_topic():
    def cell(run, dom, la, r):
        return {"run": run, "domain": dom, "layer": la, "lens_size": 1.0, "rr_lens": {"1.0": {"rate": r}}}

    prim = C.primary_cells([cell("a", "el", 44, 0.3), cell("a", "el", 46, 0.4), cell("a", "co", 36, 0.25)])
    assert [(c["domain"], c["layer"]) for c in prim] == [("co", 36), ("el", 46)]


def _cl(values: dict[tuple[str, str], float], fam: str = "RL") -> dict:
    return {
        (fam, s, d): {"n": 100, "right": (v, v - 0.05, v + 0.05), "list": 0.0, "off": 0.0}
        for (s, d), v in values.items()
    }


def test_parts_verdicts():
    base = {(s, d): 0.98 for s in P.PARTS for d in ("question", "final")}
    name_q = {**base, ("lookup", "question"): 0.30, ("lookup_name", "question"): 0.40, ("lookup", "final"): 0.05,
              ("lookup_digit", "final"): 0.10}  # fmt: skip
    v = P.verdicts(_cl(name_q))
    assert v["valid"] and v["question_testable"] and v["H-name-q"] and not v["H-digit-q"]
    assert v["H-digit-final"] and not v["H-name-final"]
    assert "H-name-q-split" not in v  # a run without the split sources
    split = {**name_q, **{(s, d): 0.98 for s in P.SPLIT for d in ("question", "final")},
             ("lookup_nodigit", "question"): 0.35, ("lookup_noname", "final"): 0.10}  # fmt: skip
    vs = P.verdicts(_cl(split))
    assert vs["valid-split"] and vs["H-name-q-split"] and vs["H-digit-final-split"]
    assert not P.verdicts(_cl({**split, ("lookup_noname", "question"): 0.50}))["H-name-q-split"]
    assert not P.verdicts(_cl({**name_q, ("lookup", "question"): 0.90}))["question_testable"]
    assert not P.verdicts(_cl({**name_q, ("lookup_off_name", "final"): 0.80}))["valid"]
