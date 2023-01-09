"""Main module."""
from functools import partial

import pandas as pd
from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from tabulate import tabulate

from better_highlighting.components.creator import (
    FormattedString,
    FormattedTableString,
)
from better_highlighting.components.lexers_and_styles.json_lexer import (
    JSONLexer,
)
from better_highlighting.components.lexers_and_styles.style_builders import (
    JSONStyle,
    SimpleStyle,
)
from better_highlighting.data_format import (
    make_it_short,
    pretty_as_iterator,
    pretty_as_text,
)


class JSONPrinter(FormattedString):
    """Data convertor to str and highlight with JSON style."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    def format(self) -> str:
        """Prepare highlighted str."""
        if self.short:
            self.target_text = make_it_short(self.target_text)

        as_string = pretty_as_iterator(self.target_text) if self.wrap else pretty_as_text(self.target_text)

        try:
            str_highlighted = highlight(
                as_string, JSONLexer(ensurenl=False), Terminal256Formatter(style=JSONStyle().style_obj)
            )
        except (AttributeError, AssertionError) as e:
            raise e from e
        return str_highlighted


class ColorFrontPrinter(FormattedString):
    """Data convertor to str and highlight with table_color and font."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    def format(self) -> str:
        """Prepare highlighted str."""
        if self.short:
            self.target_text = make_it_short(self.target_text)

        as_string = pretty_as_iterator(self.target_text) if self.wrap else pretty_as_text(self.target_text)

        try:
            str_highlighted = highlight(
                as_string,
                JSONLexer(ensurenl=False),
                Terminal256Formatter(style=SimpleStyle(self.color_front).style_obj),
            )
        except (AttributeError, AssertionError) as e:
            raise e from e
        return str_highlighted


class TablePrinter(FormattedTableString):
    """Data convertor to str and highlight with Table."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)

    def format(self) -> str:
        """Prepare highlighted str."""
        data_to_process = (
            (make_it_short(self.target_text, nested=True) if self.short else self.target_text)
            if isinstance(self.target_text, list)
            else [make_it_short(self.target_text, nested=True) if self.short else self.target_text]
        )

        data_frame = pd.DataFrame(data_to_process)

        data_frame.columns = [f"||{str(column).upper()}||" for column in data_frame.columns]

        for column in data_frame.columns:
            data_frame[column] = data_frame[column].apply(partial(pretty_as_iterator, htchar=" "))

        table_as_list = [
            highlight(
                tabulate(
                    **{
                        "tabular_data": data_frame.iloc[i : i + 4].transpose()
                        if self.transpose
                        else data_frame.iloc[i : i + 4],
                        "showindex": self.show_headers,  # True if transpose else False,
                        "tablefmt": "fancy_grid",
                        "colalign": ("left",),
                    }
                ),
                JSONLexer(),
                Terminal256Formatter(style=JSONStyle(self.color_front).style_obj),
            ).replace("||", "  ")
            for i in range(0, len(data_frame), 4)
        ]

        return f'{"↑" * 103}\n{"↓" * 103}\n'.join(table_as_list)
