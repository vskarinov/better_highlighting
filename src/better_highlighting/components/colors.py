"""Color types."""
from typing import NewType

Color = NewType("Color", str)


class Dark:
    """Supported 'Dark' colors."""

    BLACK = Color("ansiblack")
    RED = Color("ansired")
    GREEN = Color("ansigreen")
    YELLOW = Color("ansiyellow")
    BLUE = Color("ansiblue")
    MAGENTA = Color("ansimagenta")
    CYAN = Color("ansicyan")
    GRAY = Color("ansigray")


class Normal:
    """Supported colors."""

    BLACK = Color("ansibrightblack")
    RED = Color("ansibrightred")
    GREEN = Color("ansibrightgreen")
    YELLOW = Color("ansibrightyellow")
    BLUE = Color("ansibrightblue")
    MAGENTA = Color("ansibrightmagenta")
    CYAN = Color("ansibrightcyan")
    WHITE = Color("ansiwhite")
