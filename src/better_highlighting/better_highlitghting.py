"""Main module."""
from itertools import product
from typing import Union

from better_highlighting.components.colors import (
    Dark,
    Normal,
)
from better_highlighting.components.creator import OutputCreator
from better_highlighting.components.fonts import Fonts
from better_highlighting.components.highlighters import (
    ColorFrontPrinter,
    JSONPrinter,
    TablePrinter,
)


class HighLightStyleColor(OutputCreator):
    """Color and font highlighter."""

    def __init__(self, color_front=None, wrap=False, short=False):
        """Init.

        Args:
            color_front: table_color and font for highlight.
            wrap: wrap result string.
            short: cut to make it short.
        """
        self.color_front = color_front
        self.wrap = wrap
        self.short = short

    def highlight(self, text: Union[dict, str, tuple, list]) -> "ColorFrontPrinter":
        """Highlight data with table_color.

        Args:
            text: data to highlight.
        """
        return ColorFrontPrinter(text, color_front=self.color_front, wrap=False, short=False)


class HighLightStyleJSON(OutputCreator):
    """JSON Style highlighter."""

    def __init__(self, wrap=False, short=False):
        """Init.

        Args:
            wrap: wrap result string.
            short: cut to make it short.
        """
        self.wrap = wrap
        self.short = short

    def highlight(self, text: Union[dict, str, tuple, list]) -> "JSONPrinter":
        """Highlight data with JSON style colors.

        Args:
            text: data to highlight.
        """
        return JSONPrinter(text, wrap=self.wrap, short=self.short)


class TableStyleJSON(OutputCreator):
    """Table highlighter."""

    def __init__(self, color_front=None, wrap=False, short=False, transpose=False, show_headers=True):
        """Init.

        Args:
            color_front: table_color and font for highlight.
            wrap: wrap result string.
            short: cut to make it short.
            transpose: transpose table.
            show_headers: show table headers.
        """
        self.color_front = color_front
        self.wrap = wrap
        self.short = short
        self.transpose = transpose
        self.show_headers = show_headers

    def highlight(
        self,
        text: Union[dict, str, tuple, list],
    ):
        """Highlight data with Table style colors wraps and intends.

        Args:
            text: data to highlight.
        """
        return TablePrinter(
            text,
            color_front=self.color_front,
            wrap=self.wrap,
            short=self.short,
            transpose=self.transpose,
            show_headers=self.show_headers,
        )


def highlight_color_font(text, color_font=None):
    """Highlight data with table_color and font.

    Args:
        text: data to highlight.
        color_font: table_color and font for highlight.
    """
    return HighLightStyleColor(color_font).highlighter(text)


def highlight_json_style(text, wrap=False, short=False):
    """Highlight data with JSON style.

    Args:
        text: data to highlight.
        wrap: wrap result string.
        short: cut to make result str short.
    """
    return HighLightStyleJSON(wrap=wrap, short=short).highlighter(text)


def tabulate_with_color_font(text, color_font=None, wrap=False, short=False, transpose=False, show_headers=True):
    """Highlight data with Table style.

    Args:
        text: data to highlight.
        color_font: table_color and font for highlight.
        wrap: wrap result string.
        short: cut to make result str short.
        transpose: transpose table.
        show_headers: show table headers
    """
    return TableStyleJSON(
        color_font, wrap=wrap, short=short, transpose=transpose, show_headers=show_headers
    ).highlighter(text)


if __name__ == "__main__":

    font_styles = [value for supported_font, value in Fonts.__dict__.items() if str(supported_font).isupper()]

    fonts_combinations = []
    buffer_font = ""
    for font_1, font_2 in product(font_styles, font_styles):
        res = f"{font_1} {font_2}"
        if font_1 != font_2 and res not in fonts_combinations and font_1 != buffer_font:
            fonts_combinations.append(res)
        buffer_font = font_2
    fonts_combinations.append(" ".join(font_styles))

    normal_colors = [value for supported_color, value in Normal.__dict__.items() if str(supported_color).isupper()]
    dark_colors = [value for supported_color, value in Dark.__dict__.items() if str(supported_color).isupper()]

    LONG_STR = (
        "This is a long string to check and demo not only table_color formatting but also "
        "functionality of long sting wrap to new line"
    )

    demo_list = ["list_element_1", "list_element_2", "list_element_3", LONG_STR]
    demo_tuple = ("tuple _element_1", "tuple_element_2", "tuple_element_3", "tuple_element_4", 1, 2)
    demo_dict = {
        "Header_1": demo_list,
        "HEADER_2": demo_tuple,
        "h_e_a_d_e_r": "some text",
        1234567: 5555888999,
        "long_value_str": LONG_STR,
    }

    print(highlight_json_style(demo_list))
    print(highlight_json_style(demo_tuple))
    print(highlight_json_style(demo_dict))
    print(highlight_json_style(LONG_STR))

    print(" ".join([highlight_color_font(color, color) for color in normal_colors + dark_colors]))
    print(" ".join([highlight_color_font(font, font) for font in font_styles + fonts_combinations]))

    print(highlight_json_style(demo_list, wrap=True))
    print(highlight_json_style(demo_tuple, wrap=True))
    print(highlight_json_style(demo_dict, wrap=True))
    print(highlight_json_style(LONG_STR, wrap=True))

    print(
        tabulate_with_color_font(demo_list, color_font=Normal.WHITE, transpose=False, show_headers=False, short=False)
    )

    print(tabulate_with_color_font(demo_dict, color_font=Normal.RED, transpose=True, show_headers=True, short=False))

    print(highlight_json_style({1234: 555}))
