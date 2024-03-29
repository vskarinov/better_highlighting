"""Styles."""
from pygments.style import StyleMeta
from pygments.token import Token

_tokens_simple = (
    Token.Text,
    Token.Name,
    Token.Punctuation,
    Token.Operator,
    Token.Number,
    Token.String,
    Token.Keyword,
    Token.Generic,
    Token.Whitespace,
    Token.Escape,
    Token.Other,
    Token.AdditionalSymbols,
    Token.Table_1,
    Token.CustomTrue,
    Token.CustomFalse,
    Token.FormatSeparator,
    Token.Null,
)


class SimpleStyle:
    """Style to highlight str with colors and fonts."""

    def __init__(self, font_style: str):
        """Init."""
        self.style_obj = StyleMeta(
            "SimpleStyle",
            (),
            {
                "__module__": self.__module__,
                "__qualname__": "Style",
                # 'background_color': '#ffffff',
                # 'highlight_color': '#ffffcc',
                # 'line_number_color': 'inherit',
                # 'line_number_background_color': 'transparent',
                # 'line_number_special_color': '#000000',
                # 'line_number_special_background_color': '#ffffc0',
                "styles": {token: font_style for token in _tokens_simple}
                if font_style
                else {token: "" for token in _tokens_simple}
                # 'web_style_gallery_exclude': False
            },
        )


class JSONStyle:
    """Style to highlight str with JSON colors and intends."""

    styles = {
        Token.Punctuation: "ansired",
        Token.String: "#ffa500",
        Token.Name: "ansigreen",  #'#ffa500',
        Token.SpecialMessages: "italic #76756C",
        Token.CustomTrue: "bold #42EB53",
        Token.CustomFalse: "bold #FF001A",
        Token.FormatSeparator: "#FFFFFF",
        Token.Text: "ansigreen",
        Token.Null: "#40ffff",
        Token.Number: "#3677a9",
    }

    def __init__(self, table_color=None):
        """Init."""
        if table_color:
            self.styles.update({Token.Table_1: table_color})
        else:
            self.styles.update({Token.Table_1: ""})

        self.style_obj = StyleMeta(
            "JSONStyle",
            (),
            {
                "__module__": self.__module__,
                "__qualname__": "Style",
                # 'background_color': '#ffffff',
                # 'highlight_color': '#ffffcc',
                # 'line_number_color': 'inherit',
                # 'line_number_background_color': '#ffffcc',#'transparent',
                # 'line_number_special_color': '#000000',
                # 'line_number_special_background_color': '#ffffc0',
                "styles": self.styles,
                # 'web_style_gallery_exclude': False
            },
        )
