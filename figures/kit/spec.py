"""The figure specs: what a figure shows, never how it looks. A Figure is a row of panels; a panel is one of five
components (Bars, Multiples, Stacked, Curves, Image). Values are cells (value, lo, hi) read from the sources by
figures/kit/data.py; colours are names resolved by the theme ("recall", "lens", "control", ...)."""

from __future__ import annotations

from dataclasses import dataclass, field

Cell = tuple  # (value, lo | None, hi | None)


@dataclass
class Series:
    label: str  # inline label (first category / line end); "" for none
    color: str  # a theme colour name
    cells: dict  # {category key: cell}
    hollow: set = field(default_factory=set)  # categories drawn hollow (after the data)
    control: bool = False  # grey, smaller, no value, no whisker


@dataclass
class Rule:
    y: float
    word: str  # written at the right end


@dataclass
class Bars:
    """T1: categories on x, one or two bars each."""

    cats: list  # [(key, name)]
    series: list  # [Series]
    ylabel: str
    ylim: tuple
    fmt: str = "{:.2f}"
    rules: list = field(default_factory=list)  # [Rule]
    band: tuple | None = None  # the random null (lo, hi)
    ticks: dict | None = None  # {cat: control value} as a grey tick
    gap: dict | None = None  # {cat: value} printed bold above the pair
    under: dict | None = None  # {cat: small grey word under the tick label}
    divider: float | None = None  # a thin vertical line between groups (x position)
    rotate: float = 0


@dataclass
class Multiples:
    """T2: one panel per model, conditions on x. Expands into len(models) panels sharing y."""

    models: list  # [(key, name)]
    conds: list  # condition names (x ticks)
    data: dict  # {model: {cond: cell}}
    colors: dict  # {cond: colour name}; "control" = grey
    ylabel: str
    ylim: tuple
    fmt: str = "{:.2f}"
    rules: list = field(default_factory=list)
    hollow: set = field(default_factory=set)  # models drawn hollow


@dataclass
class Stacked:
    """T3: 100% stacked bars, <= 4 segments [(label, colour, {cat: share})]."""

    cats: list
    segments: list
    ylabel: str
    hollow: set = field(default_factory=set)
    rotate: float = 0


@dataclass
class Line:
    label: str
    color: str
    xs: list
    ys: list
    lo: list | None = None
    hi: list | None = None
    thin: bool = False  # after the data
    mark: dict | None = None  # {x: y} points to mark with a dot and their value
    values: bool = False  # print the value at every point


@dataclass
class Curves:
    """T4: one panel per entry of `panels` [(name, [Line])]; no markers but `mark`."""

    panels: list
    xlabel: str
    ylabel: str
    ylim: tuple
    xlim: tuple | None = None
    xticks: list | None = None
    rules: list = field(default_factory=list)
    band: tuple | None = None
    vline: tuple | None = None  # (x, word)


@dataclass
class Image:
    path: str
    crop: tuple | None = None  # (top fraction, bottom fraction)


@dataclass
class Figure:
    id: str
    claim: str  # one sentence: the README's bold title; on a slide the slide title carries it
    caption: str  # what was done, n, hollow marks, sources: CAPTIONS.md / the speaker notes
    panels: list  # [Bars | Multiples | Stacked | Curves | Image]
    size: str = "full"  # full / half / third
    widths: list | None = None  # relative panel widths
