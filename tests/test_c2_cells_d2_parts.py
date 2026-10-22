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
    rl_names = [f"rl{i}" for i in range(30)]
    rl_cases = {**cases, **_cases(rl_names, 3)}
    rl = (_rows("RL", "elements", 44, "patch", None, 9, 30, rl_names)
          + _rows("RL", "elements", 44, "lens", 1.0, 0, 30, rl_names)
          + _rows("RL", "elements", 44, "random", 1.0, 0, 30, rl_names))  # fmt: skip
    out = C.reveal_cell(cells[44], rl_cases, good + rl)
    assert out["c2_lens"] and out["rl_patch"]["k"] == 9 and len(out["rl_entities"]) == 30
    lens_moves = rl[:30] + _rows("RL", "elements", 44, "lens", 1.0, 6, 30, rl_names) + rl[60:]
    assert not C.reveal_cell(cells[44], rl_cases, good + lens_moves)["c2_lens"]
    ident = _rows("RL", "elements", 44, "ident", 1.0, 6, 30, rl_names) + _rows(
        "RR", "elements", 44, "ident", 1.0, 10, 40, names
    )
    b = C.reveal_cell(cells[44], rl_cases, good + rl + ident)
    assert b["two_codes"] and b["rl_ident"]["k"] == 6 and b["rr_ident"]["k"] == 10
    weak_rr = _rows("RL", "elements", 44, "ident", 1.0, 6, 30, rl_names) + _rows(
        "RR", "elements", 44, "ident", 1.0, 4, 40, names
    )
    assert not C.reveal_cell(cells[44], rl_cases, good + rl + weak_rr)["two_codes"]  # not a bridge code: recall 10%


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
    assert not P.verdicts(_cl({**name_q, ("lookup", "question"): 0.90}))["question_testable"]
    assert not P.verdicts(_cl({**name_q, ("lookup_off_name", "final"): 0.80}))["valid"]
