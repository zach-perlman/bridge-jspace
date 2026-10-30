"""The one palette and the style rules of every figure in the repo (Dan, 30 Oct: the same colour for the same concept in
all README.md files). docs/shared/figure_style.md explains the logic; this module is its single source: the figure kit
(figkit/dottable.py), the depth story figures (scripts/story_style.py) and the audit of the embedded figures
(scripts/check_style.py) all read it.

A colour is a role, never a model or a panel. Black, purple, teal, orange and blue are the five roles a reader has to
learn; grey is everything secondary; the other shades are variants of those roles or neutral roles of their own.
"""

from __future__ import annotations

# ---- roles: what is drawn ------------------------------------------------------------------------------------------
ROLE = {
    "recall": "#2B2B2B",  # the recall reader, and what it loses
    "lookup": "#6B5BD2",  # the lookup reader
    "lens": "#1A9E8A",  # the lens part (the J++ part, the lens's directions)
    "address": "#E08A1E",  # the address, and the position route (where an item's sentence sits)
    "identity": "#3A7DC9",  # the identity route (which item it is), and an item change
    "control": "#A8A8A8",  # a control or baseline: a random part, a rotated part, a layout-only probe; grey only
    "other": "#D9D9D9",  # the remainder of a stack that is none of the above
}
# variants and neutral roles
SHADE = {
    "lookup_light": "#B8B0EA",  # a second condition of the lookup (made-up facts)
    "lookup_dark": "#3F3489",  # a second condition of the lookup (question after the scene)
    "neutral": "#4A5F6A",  # a method or quantity that is none of the roles (a supervised probe's subspace, the value)
    "mention": "#8C6D46",  # the bridge's mention (a position in the prompt)
    "question": "#B8689A",  # the question (a position in the prompt)
    "answer": "#B8433A",  # the answer word (the readout's, in the lens-readout figures); never next to a green
}
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
BREADTH_ONLY = ("DeepSeek", "Ministral", "Bolt", "OLMo")

# every colour a figure may draw in a hue (greys aside)
ALLOWED = {c.lower() for c in (*ROLE.values(), *SHADE.values(), INK, MUTED)}
