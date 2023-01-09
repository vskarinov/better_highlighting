# pylint: disable=line-too-long,missing-module-docstring # noqa: D104,E501
import sys

from better_highlighting.better_highlitghting import (
    highlight_color_font,
    highlight_json_style,
)

if sys.version_info < (3, 7):
    raise EnvironmentError("Python 3.7 or above is required.")
