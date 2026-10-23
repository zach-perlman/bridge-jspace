"""scripts/figs/split_depth (F1): J-dependence from rows, the split rule, the verdict-file check; on the real runs
(skipped when not pulled) the drawn splits and two spot values recomputed from counts, and MAIN/FULL save without an
overlap error."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.figs import split_depth as SD


def rows(path: Path, spec: dict[tuple[str, str, int], dict[str, int]], n: int = 20) -> None:
    """outcomes.jsonl with n items per (family, set, layer); spec gives each part's number switched (role b)."""
    out = []
    for (fam, where, la), parts in spec.items():
        for i in range(n):
            for part, k in parts.items():
                out.append({"family": fam, "name": f"{fam}-{i}", "set": where, "layer": la, "part": part,
                            "source": "cf", "null": False, "role": "b" if i < k else "A"})  # fmt: skip
                out.append({**out[-1], "null": True, "role": "b"})  # nulls are never counted
    path.parent.mkdir(parents=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in out))


def test_dependence_and_split(tmp_path: Path):
    spec = {
        ("PP", "bridge_word", 6): {"full": 20, "not_jspace": 2, "not_rand_sub": 18},  # needs J: 0.9
        ("PM", "bridge_word", 6): {"full": 20, "not_jspace": 2, "not_rand_sub": 20},
        ("PP", "bridge_word", 8): {"full": 20, "not_jspace": 17, "not_rand_sub": 16},  # at the random level
        ("PM", "bridge_word", 8): {"full": 20, "not_jspace": 4, "not_rand_sub": 20},  # recalls well above
    }
    rows(tmp_path / "sp" / "run" / "outcomes.jsonl", spec)
    cells = SD.load(tmp_path / "sp", (("9b", "run", "bridge_word", (6, 8), False, False),), tmp_path / "none")
    assert [round(c.dep["lookups"].value, 3) for c in cells] == [0.9, 0.15]
    assert round(cells[1].rand["lookups"].value, 3) == 0.2 and round(cells[1].dep["recalls"].value, 3) == 0.8
    assert SD.split_of(cells) == 8
    assert SD.split_of(cells[:1]) is None  # lookups far above the random level


def test_verdict_mismatch_raises(tmp_path: Path):
    rows(tmp_path / "sp" / "run" / "outcomes.jsonl", {("PP", "bridge_word", 6): {"full": 10, "not_jspace": 5}})
    v = tmp_path / "v" / "x"
    v.mkdir(parents=True)
    v.joinpath("verdict.json").write_text(json.dumps(
        {"parts": "run", "cells": {"bridge_word:6": {"lookup": {"full": [0.6, 0, 1, 20]}}}}))  # fmt: skip
    SD.verdict_cells.cache_clear()
    with pytest.raises(ValueError, match="verdict file"):
        SD.load(tmp_path / "sp", (("9b", "run", "bridge_word", (6,), False, False),), tmp_path / "v")
    SD.verdict_cells.cache_clear()


def test_real_runs(tmp_path: Path):
    if not all((SD.SP / run / "outcomes.jsonl").exists() for _, run, *_ in SD.CELLS):
        pytest.skip("parts runs not pulled")
    cells = SD.load()
    assert SD.splits(cells) == {"9b": 12, "27b": 32, "122b": 33, "olmo": None}
    at = {(c.model, c.where, c.layer): c for c in cells}
    assert at[("9b", "bridge_word", 12)].dep["lookups"].value == pytest.approx((85 - 70) / 85)
    assert at[("27b", "bridge_word", 16)].dep["recalls"].value == pytest.approx((176 - 14) / 176)
    for kind in ("main", "full"):
        fr, nums = SD.figure(kind, cells)
        SD.C.save(fr, SD.STEM, nums, tmp_path)
        assert (tmp_path / "data" / f"{SD.STEM}_{kind}.json").exists()
