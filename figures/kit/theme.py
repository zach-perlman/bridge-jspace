"""Themes: every visual choice in one place. Change a colour, a font size or the rule's style here and every figure
follows. A target (slide / readme) picks its theme and decides which texts a figure carries."""

from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Theme:
    name: str
    colors: dict = field(default_factory=lambda: {
        "recall": "#2B2B2B", "lookup": "#6B5BD2", "lens": "#1A9E8A", "address": "#E08A1E", "identity": "#3A7DC9",
        "control": "#BDBDBD", "rule": "#8C8C8C", "dark": "#595959"})  # fmt: skip
    axis: float = 13  # axis titles
    tick: float = 12
    label: float = 12  # inline series labels
    value: float = 11  # values on key marks; nothing smaller anywhere
    sizes: dict = field(default_factory=lambda: {"full": (11, 4.4), "half": (5.4, 4.4), "third": (3.7, 4.4)})
    dpi: int = 160
    title: bool = False  # the README carries one bold claim above the figure; slides carry none
    title_size: float = 14
    rule_style: dict = field(default_factory=lambda: {"ls": "--", "lw": 1.2})
    band_alpha: float = 0.3
    control_scale: float = 0.7  # controls: smaller, grey, no value
    bar_width: float = 0.8
    whisker: dict = field(default_factory=lambda: {"color": "black", "lw": 1.1})

    def c(self, key: str) -> str:
        """A colour by name (who / what), or a literal hex."""
        return self.colors.get(key, key)


README = Theme("readme", title=True)
SLIDE = replace(Theme("slide"), axis=14, tick=13, label=13, value=12, dpi=200,
                sizes={"full": (12.3, 5.3), "half": (6.0, 5.3), "third": (4.0, 5.3)})  # fmt: skip
THEMES = {"readme": README, "slide": SLIDE}
