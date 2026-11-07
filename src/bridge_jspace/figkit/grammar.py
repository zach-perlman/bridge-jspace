"""Figure grammar v2 (docs/shared/figure_style.md): the marks a v2 figure draws, each tagged with its role and status,
the key built from what is drawn, numbers formatted by unit, and the checks that test meaning, not only membership.

A v2 figure draws every mark through `mark`, `tick`, `band`, `rule` or `connector`, names every role colour by a
coloured word (`role_word`), prints numbers through `num`, and takes its key from `key()`. `check` then fails on:
a mark whose colour is not ROLE[its tag] (1), a role colour on a mark of another role or a legacy shade (2), a hollow
mark whose cell is not post hoc in data/figures/status.csv or the reverse, a status tag that disagrees with it (3), an
encoding drawn but not named or named but not drawn (4), a word outside figkit/terms.py (5), a cue not "→ more …" (6).
Number strings are logged by data key; tests/test_figure_grammar.py checks one key prints one string everywhere (7)."""

from __future__ import annotations

import csv
import re
from functools import cache

from matplotlib.colors import to_hex
from matplotlib.patches import Rectangle

from bridge_jspace.figkit import terms
from bridge_jspace.figkit.data import REPO
from bridge_jspace.palette import BAND, GRID, LEGACY, MUTED, ROLE

STATUS_CSV = REPO / "data" / "figures" / "status.csv"
STATUSES = ("fixed_in_advance", "post_hoc", "descriptive", "not_claimed")
CHROME = {"#d6d6d6", "#8c8c8c", GRID.lower(), BAND.lower(), "#bdbdbd", "#ffffff"}  # connectors, rules, grid, band

FIGURE = {"id": "", "defer_key": False}  # the figure being drawn (set by `begin`); defer_key: an upper stacked panel
# whose encodings the last panel's key names (the key check runs on the last panel, with every panel's encodings)
DRAWN: dict[str, set] = {"control": set(), "tick": set(), "post_hoc": set(), "whisker": set(), "band": set()}
NUMBERS: list[tuple[str, str, str]] = []  # (figure, data key, printed string) of every number a v2 figure prints
CVD: dict[str, list] = {}  # figure -> role-colour pairs under the colour-vision floors (check 8; reported, not fixed)


def begin(fig_id: str) -> None:
    """Start a figure: its id names its cells in the status registry; the drawn encodings start empty."""
    FIGURE["id"], FIGURE["defer_key"] = fig_id, False
    for v in DRAWN.values():
        v.clear()


# ---- the status registry (B) -----------------------------------------------------------------------------------------
@cache
def registry() -> dict[tuple[str, str], dict]:
    with STATUS_CSV.open() as f:
        return {(r["figure"], r["cell"]): r for r in csv.DictReader(f)}


def status(cell: str, fig_id: str | None = None) -> str:
    """A drawn cell's status, from data/figures/status.csv (a cell missing there is an error, not a default)."""
    key = (fig_id or FIGURE["id"], cell)
    if key not in registry():
        raise KeyError(f"no status for {key} in {STATUS_CSV.relative_to(REPO)}")
    return registry()[key]["status"]


def _tag(artists, **g) -> None:
    for a in artists:
        a._g = g


# ---- marks (C) -------------------------------------------------------------------------------------------------------
def mark(ax, x, y, role: str, cell: str, interval=None, size: float = 9.5, name: str = "", zorder: float = 4):
    """A dot (an estimate) in its role colour, hollow if its cell is post hoc in the registry, with a same-colour
    whisker for its 95% interval. A control's dot (role 'control') names its control in `name` (the key's "grey: …")."""
    st = status(cell)
    col = ROLE[role]
    if interval is not None and interval[0] is not None:
        _tag(ax.plot([interval[0], interval[1]], [y, y], color=col, lw=1.8, solid_capstyle="butt", zorder=zorder - 1),
             kind="whisker", role=role, cell=cell)  # fmt: skip
        DRAWN["whisker"].add(cell)
    hollow = st == "post_hoc"
    _tag(ax.plot([x], [y], "o", ms=size, color=col, mfc="white" if hollow else col, mew=2 if hollow else 0,
                 zorder=zorder), kind="dot", role=role, cell=cell, status=st, hollow=hollow)  # fmt: skip
    if hollow:
        DRAWN["post_hoc"].add(cell)
    if role == "control":
        DRAWN["control"].add(name or "a control")
    return st


def tick(ax, x, y, half: float = 0.26) -> None:
    """The largest same-size control: a grey tick on the estimate's own axis."""
    _tag(ax.plot([x, x], [y - half, y + half], color=ROLE["control"], lw=2.4, zorder=3), kind="tick", role="control")
    DRAWN["tick"].add(1)


def band(ax, n: int, lo: float = -0.1, hi: float = 0.1) -> None:
    """The light-grey band at zero: within 0.10 of a random part."""
    r = Rectangle((lo, -0.5), hi - lo, n, color=BAND, zorder=0.5, lw=0)
    ax.add_patch(r)
    _tag([r], kind="band", role="chrome")
    DRAWN["band"].add(1)


def rule(ax, x, n: int, skip=()) -> None:
    """A dashed grey reference line (its label goes above the first row, a canonical phrase)."""
    from bridge_jspace.figkit.dottable import runs

    for a, b in runs(n, skip):
        _tag(ax.plot([x, x], [b - 0.5, a - 0.5], color="#8C8C8C", ls=(0, (4, 3)), lw=1.1, zorder=1), kind="rule",
             role="chrome")  # fmt: skip


def connector(ax, a, b, y) -> None:
    _tag(ax.plot([a, b], [y, y], color="#D6D6D6", lw=3.2, solid_capstyle="round", zorder=2), kind="connector",
         role="chrome")  # fmt: skip


def role_word(ax, x, text: str, role: str, ha: str = "center", level: int = 0) -> None:
    """The coloured word that names a role colour, above the first row (E1); level 1 sits under level 0, nearer the
    first row, for a second word that would not fit beside the first."""
    top = ax.get_ylim()[1]
    y = -0.5 + (0.72 if level == 0 else 0.25) * (top + 0.5)
    t = ax.text(x, y, text, ha=ha, va="center", fontsize=_head_size(), color=ROLE[role], weight="bold")
    t._g = {"kind": "role_word", "role": role}


def _head_size() -> float:  # the dot table's head-label size (the target's theme)
    from bridge_jspace.figkit.dottable import FS

    return FS["head"]


def tag_text(t, cell: str, tag: str) -> None:
    """Mark a status tag ("descriptive", "not claimed: …") drawn in a cell, for the registry check."""
    t._g = {"kind": "status_tag", "cell": cell, "tag": tag}


# ---- numbers (G) -------------------------------------------------------------------------------------------------------
FORMAT = {"accuracy": "{:.0f}", "points": "{:.1f}", "share": "{:.2f}", "multiple": "{:.2f}", "z": "{:.0f}"}


def num(key: str, value: float, unit: str, sign: bool = False) -> str:
    """A number as every figure prints it for its unit (one precision per unit), logged by its data key."""
    fmt = FORMAT[unit].replace("{:", "{:+") if sign else FORMAT[unit]
    s = fmt.format(value).replace("-", "−")
    s = "0" + s[2:] if s.startswith("−0") and set(s[1:]) <= set("0.") else s  # no "−0.0"
    NUMBERS.append((FIGURE["id"], key, s))
    return s


def interval(key: str, lo: float, hi: float, unit: str) -> str:
    return f"[{num(key + '.lo', lo, unit)}, {num(key + '.hi', hi, unit)}]"


def count(key: str, k: int, n: int) -> str:
    s = f"{k} of {n}"
    NUMBERS.append((FIGURE["id"], key, s))
    return s


# ---- the key (E) ---------------------------------------------------------------------------------------------------------
def key() -> list:
    """One key line from what was drawn, in the fixed order, with the fixed phrases (E2)."""
    parts = []
    if DRAWN["control"]:
        parts.append(("●", ROLE["control"], terms.KEY_CONTROL.format(" · ".join(sorted(DRAWN["control"])))))
    if DRAWN["tick"]:
        parts.append(("", MUTED, terms.KEY_TICK))
    if DRAWN["post_hoc"]:
        parts.append(("", MUTED, terms.KEY_POST_HOC))
    if DRAWN["whisker"]:
        parts.append(("", MUTED, terms.KEY_WHISKER))
    if DRAWN["band"]:
        parts.append(("", MUTED, terms.KEY_BAND))
    rows, n = [[]], 0  # one line; a second when it would not fit the 8 in width at the key's size (~95 characters)
    for p in parts:
        w = len(p[0]) + len(p[2]) + 6
        if rows[-1] and n + w > 95:
            rows.append([])
            n = 0
        rows[-1].append(p)
        n += w
    return rows if parts else []


# ---- the checks ----------------------------------------------------------------------------------------------------------
def _hex(c) -> str | None:
    try:
        return to_hex(c).lower()
    except (ValueError, TypeError):
        return None


ROLE_HEX = {v.lower(): k for k, v in ROLE.items()}
LEGACY_HEX = {v.lower() for v in LEGACY.values()}


def check(fig, name: str, fig_id: str | None = None) -> list[str]:
    """Grammar v2's meaning checks (1-6) on a saved figure's artists."""
    fid = fig_id or FIGURE["id"]
    out = []
    marks_roles, texts = set(), []
    for ax in fig.axes:
        for a in [*ax.lines, *ax.patches, *ax.collections]:
            g = getattr(a, "_g", None)
            cols = {_hex(c) for c in _colours(a)} - {None}
            for c in cols & LEGACY_HEX:
                out.append(f"{name}: legacy shade {c} (a shade never encodes a variable)")
            if g is None:
                for c in cols:
                    if c in ROLE_HEX and ROLE_HEX[c] not in ("other",) and c not in CHROME:
                        out.append(f"{name}: an untagged mark in the {ROLE_HEX[c]} colour {c}")
                continue
            if g["role"] in ROLE:
                want = ROLE[g["role"]].lower()
                for c in cols - {"#ffffff"}:
                    if c != want:
                        out.append(f"{name}: a {g['kind']} tagged {g['role']} drawn in {c}, not {want}")
                if g["role"] not in ("control", "other"):
                    marks_roles.add(g["role"])
            if g["kind"] == "dot":
                post_hoc = registry()[(fid, g["cell"])]["status"] == "post_hoc"
                if g["hollow"] != post_hoc:
                    out.append(f"{name}: cell {g['cell']} drawn {'hollow' if g['hollow'] else 'filled'}, registry says "
                               f"{registry()[(fid, g['cell'])]['status']}")  # fmt: skip
        texts += ax.texts
    texts += fig.texts
    all_texts = [t for t in fig.findobj(match=lambda a: hasattr(a, "get_text") and hasattr(a, "get_rotation"))
                 if t.get_text().strip() and t.get_visible()]  # fmt: skip
    # 1/2 and E1: every role drawn is named by a word in its colour; a coloured word names a role that is drawn
    word_roles = {ROLE_HEX.get(_hex(t.get_color())) for t in all_texts} - {None, "control", "other", "recall"}
    names_all = fid == "key"  # the key figure names every role by design
    for r in sorted(marks_roles - {"recall"}):
        if r not in word_roles:
            out.append(f"{name}: the {r} colour is drawn but no word in it names it")
    for r in sorted(word_roles - marks_roles if not names_all else ()):
        out.append(f"{name}: a word in the {r} colour, but no {r} mark")
    # 3: status tags agree with the registry, both ways (a descriptive cell says so; a cell the post does not claim
    # carries the registry's "not claimed: <reason>")
    tagged = {}
    for t in all_texts:
        g = getattr(t, "_g", None)
        if g and g.get("kind") == "status_tag":
            tagged[g["cell"]] = g["tag"]
    drawn_cells = {a._g["cell"] for ax in fig.axes for a in ax.lines if getattr(a, "_g", {}).get("kind") == "dot"}
    for cell in drawn_cells | set(tagged):
        r = registry()[(fid, cell)]
        want = terms.DESCRIPTIVE if r["status"] == "descriptive" else r["tag"]
        if tagged.get(cell, "") != want:
            out.append(f"{name}: cell {cell} tagged {tagged.get(cell, '')!r}, the registry says {want!r}")
    # 4: key completeness, both ways
    words = " ".join(t.get_text() for t in all_texts)
    for k, phrase in () if FIGURE["defer_key"] else (("tick", terms.KEY_TICK), ("post_hoc", terms.KEY_POST_HOC), ("whisker", terms.KEY_WHISKER),
                      ("band", terms.KEY_BAND)):  # fmt: skip
        if bool(DRAWN[k]) != (phrase in words):
            out.append(f"{name}: {phrase!r} {'drawn but not named' if DRAWN[k] else 'named but not drawn'}")
    if not FIGURE["defer_key"] and bool(DRAWN["control"]) != ("grey: " in words):
        out.append(f"{name}: a control {'drawn but not named' if DRAWN['control'] else 'named but not drawn'}")
    # 8: colour vision, on the role colours this figure draws (marks, and grey if a control is drawn)
    from bridge_jspace.figkit.colour_vision import failures

    drawn = {r: ROLE[r] for r in marks_roles | ({"control"} if DRAWN["control"] or DRAWN["tick"] else set())}
    if fails := failures(drawn):
        CVD[fid] = fails
    # 5, 6: words and cues
    for t in all_texts:
        s = t.get_text()
        if not terms.allowed(s):
            out.append(f"{name}: text not in figkit/terms.py {s[:40]!r}")
        for b in terms.banned(s):
            out.append(f"{name}: banned word in {s[:30]!r} ({b})")
    for ax in fig.axes:
        c = getattr(ax, "_cue", "")
        if c and not re.match(r"^→ more ", c):
            out.append(f"{name}: cue {c!r} is not '→ more …'")
    return sorted(set(out))


def _colours(a):
    for getter in ("get_color", "get_markerfacecolor", "get_markeredgecolor", "get_facecolor", "get_edgecolor"):
        f = getattr(a, getter, None)
        if f is None:
            continue
        try:
            c = f()
        except Exception:
            continue
        if isinstance(c, str) or (hasattr(c, "__len__") and len(c) in (3, 4) and not hasattr(c[0], "__len__")):
            yield c
