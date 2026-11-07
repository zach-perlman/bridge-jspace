"""The one palette and the style rules of every figure in the repo (Dan, 30 Oct: the same colour for the same concept in
all README.md files). docs/shared/figure_style.md explains the logic; this module is its single source: the figure kit
(figkit/dottable.py), the depth story figures (scripts/story_style.py) and the audit of the embedded figures
(scripts/check_style.py) all read it.

A colour is a role, never a model, a panel or a variable (grammar v2, 7 Nov): one hue per role in ROLE; grey is a
control and nothing else; a status (post hoc, descriptive, not claimed) is never a colour.
"""

from __future__ import annotations

# ---- roles: what is drawn (figure grammar v2, docs/shared/figure_style.md A) ---------------------------------------
# one hue per role; a shade never encodes a variable (a second condition of a reader is its own column, named in words)
ROLE = {
    "recall": "#2B2B2B",  # the recall reader, and what it loses
    "lookup": "#6B5BD2",  # the lookup reader, only
    "lens": "#1A9E8A",  # the lens part (any J++ directions read at a word, the city's included)
    "address": "#E08A1E",  # the address and the position route; anything measured under an address swap
    "identity": "#3A7DC9",  # the identity route; a change of item
    "answer": "#B8433A",  # the answer span, the answers' own directions, the answer word; never next to a green
    "neutral": "#4A5F6A",  # a method that is none of the roles (a supervised probe's subspace, a data-built subspace)
    "mention": "#8C6D46",  # the bridge's mention, only where rows or columns are places in the prompt
    "question": "#B8689A",  # the question, only where rows or columns are places in the prompt
    "control": "#A8A8A8",  # a control or baseline, and nothing else
    "other": "#D9D9D9",  # the remainder of a 100% stack; chrome
}
# v1's shades that encoded a variable (made-up facts, question order): grammar v2 deletes them. Only the builders of the
# frozen deck (figures/slides/) and the v1 README builders (until they are redrawn) still read them; the v2 checks fail
# on any of these hexes.
LEGACY = {"lookup_light": "#B8B0EA", "lookup_dark": "#3F3489", "recall_light": "#6E6E6E"}
# v1 name for the non-reader roles plus the legacy shades, kept so the v1 builders still import
SHADE = {**{k: ROLE[k] for k in ("neutral", "mention", "question", "answer")}, **LEGACY}
# text and chrome: three text levels (bold ink, ink, grey), grid, zebra stripes, the "within 0.10" band
INK, MUTED, FAINT, GRID, ZEBRA, BAND = "#1A1A1A", "#6B6B6B", "#BDBDBD", "#E4E4E4", "#F5F5F5", "#E6E6E6"
# greys that mean "secondary" (a darker control, a thin segment, a connector, a band); never a role
GREYS = {"#C8C8C8", "#EFE9FB", "#7A7A7A", "#9E9E9E", "#DADADA", "#D6D6D6", "#8C8C8C", "#E6E6E6", "#E4E4E4", "#F5F5F5", "#BDBDBD", "#6B6B6B"}

# ---- marks and order ----------------------------------------------------------------------------------------------------
HOLLOW_WORD = "post hoc"  # a hollow marker (○) means this and nothing else; every figure that uses one says so
MODELS = (  # one model order everywhere; then the breadth-only models
    ("qwen3.5-9b", "Qwen 9B"),
    ("qwen3.6-27b", "Qwen 27B"),
    ("muse-glimmer-30b", "Muse 30B"),
    ("nemotron-3.5-lightning", "Lightning"),
    ("qwen3.5-122b-a10b", "Qwen 122B"),
)
BREADTH_ONLY = ("DeepSeek", "Ministral", "Bolt", "OLMo", "Qwen3-32B", "Olmo-Hybrid 7B", "Olmo-3 7B")

# every colour a figure may draw in a hue (greys aside)
ALLOWED = {c.lower() for c in (*ROLE.values(), *SHADE.values(), INK, MUTED)}
