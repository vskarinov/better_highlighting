"""Abstract level module (Fabric methodology)."""
from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import Union


class OutputCreator(ABC):
    """Main creator of highlighted str."""

    @abstractmethod
    def highlight(self, text: Union[dict, str, tuple, list]):
        """Process data by conversion it to str and adding special simbols according to formatting style."""

    def highlighter(self, text) -> str:
        """Call for formatter."""
        return self.highlight(text).format()


class FormattedString(ABC):
    """Concrete creator for str formatted by table_color, font or JSON Style."""

    def __init__(self, target_text, wrap=False, short=False, color_front="white"):
        """Init."""
        self.target_text = target_text
        self.wrap = wrap
        self.short = short
        self.color_front = color_front

    @abstractmethod
    def format(self) -> str:
        """Prepare highlighted str."""


class FormattedTableString(ABC):
    """Concrete creator for str formatted by Table Style."""

    def __init__(
        self, target_text, wrap=False, short=False, color_front="ansiwhite", transpose=False, show_headers=False
    ):
        """Init."""
        self.target_text = target_text
        self.wrap = wrap
        self.short = short
        self.color_front = color_front
        self.transpose = transpose
        self.show_headers = show_headers

    @abstractmethod
    def format(self) -> str:
        """Prepare highlighted str."""
