"""Pytest configuration and resources."""
from pygments.console import (
    dark_colors,
    esc,
    light_colors,
)

COLORS = {}

for x, (d, l) in enumerate(zip(dark_colors, light_colors), start=30):
    COLORS[f"ansi{d}"] = f"{esc}{x}m"  # esc + "%im" % x
    COLORS[f"ansi{l}"] = f"{esc}{60+x}m"  # esc + "%im" % (60 + x)

COLORS["ansiwhite"] = f"{esc}01m"

FONTS = {d: f"{esc}0{(x if x == 1 else x + 1)}m" for x, d in enumerate(["bold", "italic", "underline"], start=1)}
