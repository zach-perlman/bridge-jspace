"""data/figures/lenses.csv (scripts/lens_csv.py): every row traces to a file that exists, and every pass@10 is the cell
its source names."""

import csv
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CSV = REPO / "data/figures/lenses.csv"


def rows() -> list[dict]:
    with CSV.open() as f:
        return list(csv.DictReader(f))


def test_keys_unique_and_every_model_has_a_kind_and_a_quality():
    rs = rows()
    keys = [r["key"] for r in rs]
    assert len(keys) == len(set(keys))
    models = {r["model"] for r in rs}
    for m in models:
        assert f"lens.{m}.kind" in keys and f"lens.{m}.passk" in keys, m


@pytest.mark.parametrize("r", rows(), ids=lambda r: r["key"])
def test_source_exists_or_not_measured(r):
    if r["value"] == "not measured":
        assert r["source"] == ""
        return
    path = r["source"].split(" | ")[0]
    assert path and (REPO / path).exists(), r["source"]


@pytest.mark.parametrize("r", [r for r in rows() if r["unit"].startswith("pass@10") and r["value"] != "not measured"],
                         ids=lambda r: r["key"])  # fmt: skip
def test_pass_at_10_is_the_named_cell(r):
    path, field = r["source"].split(" | ")
    want = dict(kv.split("=") for kv in field.split(", "))
    with (REPO / path).open() as f:
        cells = [d["pass_at_k"] for d in csv.DictReader(f) if all(d[k] == v for k, v in want.items())]
    assert len(cells) == 1 and f"{float(cells[0]):.3f}" == r["value"]
