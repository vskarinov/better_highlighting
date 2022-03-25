from pygments import highlight
from typing import Optional, Union
from tabulate import tabulate
from functools import partial
import pandas as pd
from better_highlighting.json_lexer import JSONLexer
from pygments.formatters import Terminal256Formatter
from better_highlighting.style_builders import SimpleStyle, JSONStyle
from better_highlighting.data_format import pretty_as_iterator, pretty_as_text, make_it_short


class __Printer:

    def __init__(self):
        self._font: str = str()
        self._colors: str = str()

    def display(self, text, colors_style: Optional[str] = None,
                font_style: Optional[str] = None,
                pretty_view=False,
                short=False):
        self._font = font_style or str()
        self._colors = colors_style or str()

        text_to_process = make_it_short(text) if short else text

        if pretty_view:
            string_to_color = pretty_as_iterator(text_to_process)
        else:
            string_to_color = pretty_as_text(text_to_process)
        try:
            print(highlight(
                string_to_color,
                JSONLexer(),
                Terminal256Formatter(style=self._style)
            ))
        except AttributeError as e:
            raise e from e

    def store(self, text, colors_style: Optional[str] = None,
              font_style: Optional[str] = None,
              pretty_view=False,
              short=False) -> str:

        self._font = font_style or str()
        self._colors = colors_style or str()

        text_to_process = make_it_short(text) if short else text

        if pretty_view:
            string_to_color = pretty_as_iterator(text_to_process)
        else:
            string_to_color = pretty_as_text(text_to_process)
        try:
            return highlight(
                string_to_color,
                JSONLexer(),
                Terminal256Formatter(style=self._style)
            )
        except AttributeError as e:
            raise e from e

    def table(self, data: Union[list, str, dict],
              colors_style: Optional[str] = None,
              short=False, transpose=False):

        data_to_process = (make_it_short(data) if short else data) \
            if isinstance(data, list) \
            else (make_it_short([data]) if short else [data])

        df = pd.DataFrame(data_to_process)

        df.columns = [f'||{str(column).upper()}||' for column in df.columns]

        for c in df.columns:
            df[c] = df[c].apply(partial(pretty_as_iterator, htchar=' '))

        if transpose:
            table_opt = {'tabular_data': df.transpose(),
                         'showindex': True,
                         'tablefmt': "fancy_grid",
                         'colalign': ("left",)
                         }
        else:
            table_opt = {'tabular_data': df,
                         'headers': df.columns,
                         'showindex': False,
                         'tablefmt': "fancy_grid",
                         'colalign': ("left",)
                         }

        highlighted = highlight(tabulate(**table_opt),
                                JSONLexer(),
                                Terminal256Formatter(style=JSONStyle(colors_style).style_obj)).replace('||', '  ')

        print(highlighted)

    @property
    def _style(self):
        if self._font == 'simple':
            self._font = str()
        if self._colors == 'json':
            return JSONStyle().style_obj
        style_cfg = f'{self._font} {self._colors}'
        return SimpleStyle(style_cfg).style_obj


printer = __Printer()

# if __name__ == '__main__':
#     font_styles = (
#         'simple',
#         'bold',
#         'italic',
#         'italic bold',
#         'underline',
#         'italic underline',
#         'bold underline',
#         'italic bold underline')
#
#     colors = (
#         # dark
#         'ansiblack',
#         'ansired',
#         'ansigreen',
#         'ansiyellow',
#         'ansiblue',
#         'ansimagenta',
#         'ansicyan',
#         'ansigray',
#         # normal
#         'ansibrightblack',
#         'ansibrightred',
#         'ansibrightgreen',
#         'ansibrightyellow',
#         'ansibrightblue',
#         'ansibrightmagenta',
#         'ansibrightcyan',
#         'ansiwhite')
#
#     demo_list = ['list_element_1', 'list_element_2', 'list_element_3', 'list_element_4']
#     demo_tuple = ('tuple _element_1', 'tuple_element_2', 'tuple_element_3', 'tuple_element_4')
#     demo_dict = {'Header_1': demo_list, 'HEADER_2': demo_tuple, 'h_e_a_d_e_r': 'some text', 1234567: 5555888999}
#
#     print(' '.join([printer.store('style', font_style=font_style).strip('\n') for font_style in font_styles]))
#
#     print(' '.join([printer.store('color', font_style=color).strip('\n') for color in colors]))
#
#     printer.display(demo_list, pretty_view=True)
#     printer.display(demo_list, colors_style='ansicyan')
#     printer.display(demo_list, colors_style='json')
#     printer.display(demo_tuple, pretty_view=True, colors_style='json')
#     printer.display(demo_tuple, colors_style='ansiyellow')
#     printer.display(demo_dict, colors_style='json')
#     printer.display(demo_dict, pretty_view=True, colors_style='json')
#
#     printer.table(demo_dict)
#     printer.table(demo_dict, transpose=True)
