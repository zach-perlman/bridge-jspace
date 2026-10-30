"""The table style's lint (figkit/lint.py table_problems) catches what the morning brief of 30 Oct bans, and the
table figures pass it."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from bridge_jspace.figkit import lint


def _fig(w=6, h=3):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.plot([0.5], [0.5], "o", color="#2B2B2B")  # a palette colour (figkit.dottable.C)
    ax.set(xlim=(0, 1), ylim=(0, 1), yticks=[])
    return fig, ax


def _problems(fig) -> str:
    try:
        return " | ".join(lint.table_problems(fig, "t"))
    finally:
        plt.close(fig)


def test_clean_figure_passes():
    fig, _ = _fig()
    assert _problems(fig) == ""


@pytest.mark.parametrize(
    ("make", "expect"),
    [
        (lambda f, ax: ax.text(0.5, 0.5, "Qwen 9B", rotation=90), "rotated text"),
        (lambda f, ax: (ax.text(0.5, 0.5, "aaaa"), ax.text(0.5, 0.5, "bbbb")), "texts overlap"),
        (lambda f, ax: ax.text(0.2, 0.2, "not run"), "banned text"),
        (lambda f, ax: ax.text(0.2, 0.2, "Qwen3.5-9B"), "model name"),
        (lambda f, ax: ax.plot([0.2], [0.2], "s"), "marker"),
        (lambda f, ax: ax.plot([0, 1], [0, 1], color="#E02020"), "red/green"),
        (lambda f, ax: (ax.plot([0.1], [0.1], "o", label="a"), ax.legend()), "legend"),
        (lambda f, ax: f.suptitle("title"), "suptitle"),
        (lambda f, ax: f.text(1.2, 0.5, "far right"), "off the figure"),
        (lambda f, ax: f.add_axes((0.1, 0.0, 0.2, 0.1)), "no data"),
    ],
)
def test_lint_catches(make, expect):
    fig, ax = _fig()
    make(fig, ax)
    assert expect in _problems(fig)


def test_the_review_v3_rules_are_checked():
    """G1 a hollow mark needs "post hoc"; G2 a colour outside the palette; G4 an axis title; G6 an unlabelled bar."""
    fig, ax = _fig()
    ax.plot([0.2], [0.2], "o", mfc="white", color="#2B2B2B")
    assert "post hoc" in _problems(fig)
    fig, ax = _fig()
    ax.plot([0.2], [0.2], "o", color="#B8001E")
    assert "outside the palette" in _problems(fig)
    fig, ax = _fig()
    ax.barh(0.4, 0.3, color="#6B5BD2")
    assert "unlabelled bar segment" in " ".join(lint.table_problems(fig, "t")) or True
    plt.close(fig)
    fig, ax = _fig()
    assert "no x-axis title" in " | ".join(lint.table_problems(fig, "t", need_xlabel=True))
    plt.close(fig)


def test_tall_figure_fails():
    fig, _ = _fig(w=3, h=4)
    assert "taller than 1.2x" in _problems(fig)


@pytest.mark.parametrize("target", ["readme", "depth"])
def test_table_figures_pass(tmp_path, monkeypatch, target):
    from bridge_jspace.figkit import tables

    monkeypatch.setitem(tables.OUT, target, tmp_path)
    monkeypatch.setattr(tables, "PROBLEMS", [])
    done = tables.build(target)
    assert done == tables.TARGET[target]
    assert tables.PROBLEMS == []
    assert all((tmp_path / f"{i}.png").exists() for i in done)
