"""Tests."""
import pytest
from conftest import (
    COLORS,
    FONTS,
)

from better_highlighting.better_highlitghting import highlight_color_font


class TestSimpleFormatting:
    """Class with tests for ste formatting with colors and font in terminal."""

    @pytest.mark.parametrize("color,code", list(COLORS.items()))
    def test_supported_colors(self, color, code):
        """Test supported colors."""
        formatted_str = highlight_color_font(color, color)
        print(formatted_str)

        string_in_utf_8 = str(formatted_str.encode("utf-8").decode("utf-8"))

        start_code, end_code = string_in_utf_8.split(color)

        assert start_code == code, f"wrong table_color code: {start_code}, expected: {code} "
        assert end_code == "\x1b[39m", f"wrong end code: {end_code}, expected: \x1b[39m"

    @pytest.mark.parametrize("font, code", list(FONTS.items()))
    def test_supported_fonts(self, font, code):
        """Test supported fonts."""
        formatted_str = highlight_color_font(font, font)
        print(formatted_str)

        string_in_utf_8 = str(formatted_str.encode("utf-8").decode("utf-8"))

        start_code, end_code = string_in_utf_8.split(font)

        assert start_code == code, f"wrong font code: {start_code}, expected: {code} "
        assert end_code == "\x1b[00m", f"wrong end code: {end_code}, expected: \x1b[00m"

    def test_not_supported_fonts(self):
        """Test not supported fonts."""
        with pytest.raises(AssertionError):
            highlight_color_font("wrong_font", "wrong_font")

    def test_not_supported_attr(self):
        """Test not supported attributes."""
        with pytest.raises(AttributeError):
            highlight_color_font(1, 1)
