"""Font types."""
from typing import NewType

Font = NewType("Font", str)


class Fonts:
    """Supported Fonts."""

    BOLD = Font("bold")
    ITALIC = Font("italic")
    UNDERLINE = Font("underline")
