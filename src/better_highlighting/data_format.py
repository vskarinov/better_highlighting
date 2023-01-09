"""Module contains functions for data conversion to str and further wrap and cut."""
# pylint: disable=line-too-long, too-many-return-statements
import configparser
import os
import sys
import textwrap as tw
from dataclasses import (
    asdict,
    is_dataclass,
)
from typing import (
    Any,
    Optional,
)

MIN_LENGTH_STR = 1024
MIN_LENGTH_LIST = 25
MIN_LENGTH_DICT = 50
MIN_LENGTH_STR_IN_DICT = 50

MODULE_PATH_CONF = os.path.abspath(sys.path[0])
config_file = os.path.join(MODULE_PATH_CONF, "better_highlight.cfg")
if os.path.isfile(config_file):
    _config = configparser.ConfigParser()
    with open(config_file, "r", encoding="utf-8") as fl:
        _config.read_file(fl)
        MIN_LENGTH_STR = int(_config.get("data_format", "MIN_LENGTH_STR"))
        MIN_LENGTH_LIST = int(_config.get("data_format", "MIN_LENGTH_LIST"))
        MIN_LENGTH_DICT = int(_config.get("data_format", "MIN_LENGTH_DICT"))
        MIN_LENGTH_STR_IN_DICT = int(_config.get("data_format", "MIN_LENGTH_STR_IN_DICT"))


def pretty_as_iterator(value, htchar=" ", lfchar="\n", indent=0, key_length=0) -> str:
    """Format provided data in str with wraps and indents.

    In result, it returns str that looks pretty iterator type.

    Args:
        value: convert to str and wrap.
        htchar: char that will be used as start indents of font_1 line.
        lfchar: char that will be use as end indents of font_1 line.
        indent: ,
        key_length: provided length of key value if data is iterator dict.
    """
    tab_key_length = 4 if key_length != 0 else 0
    indent += 1
    nlch = lfchar + htchar * indent
    if isinstance(value, dict):
        items = [
            nlch
            + repr(key)
            + ": "
            + pretty_as_iterator(value[key], htchar, lfchar, indent + 1, key_length=len(str(key)))
            for key in value
        ]
        return f'{",".join(items) + lfchar}'  # "{%s}" % (",".join(items) + lfchar)  # + htchar * indent)
    if isinstance(value, list):
        items = [nlch + pretty_as_iterator(item, htchar, lfchar, indent + 1, key_length=0) for item in value]
        return f"[{','.join(items) + lfchar + htchar * indent}]"
    if isinstance(value, tuple):
        items = [nlch + pretty_as_iterator(item, htchar, lfchar, indent + 1, key_length=0) for item in value]
        return f"({','.join(items) + lfchar + htchar * indent})"
    if isinstance(value, str):
        width = MIN_LENGTH_STR_IN_DICT - (len(lfchar) + len(htchar) * (indent + (key_length + tab_key_length)))
        value = tw.wrap(value, width=width + 1)

        return f" {lfchar + htchar * (indent + key_length)}  ".join(value)
        # return f"{lfchar + htchar * (indent + (key_length + tab_key_length))}+".join(value) #For table format
    if isinstance(value, int):
        width = MIN_LENGTH_STR_IN_DICT - (len(lfchar) + len(htchar) * (indent + (key_length + tab_key_length)))
        value = tw.wrap(str(value), width=width + 1)
        return f" {lfchar + htchar * (indent + key_length)}+".join(value)
    return repr(value)


def pretty_as_text(value) -> str:
    """Format provided data in str.

    Args:
        value: convert to str.
    """
    if isinstance(value, dict):
        items = [f"{repr(key)}: {pretty_as_text(value[key])}" for key in value]
        return f'{", ".join(items)}'
    if isinstance(value, list):
        items = [pretty_as_text(item) for item in value]
        return f"[{', '.join(items)}]"
    if isinstance(value, tuple):
        items = [pretty_as_text(item) for item in value]
        return f"({', '.join(items)})"
    if isinstance(value, str):
        value = tw.wrap(value)
        return " ".join(value)

    return repr(value)


def make_it_short(value: Any, nested: Optional[bool] = False):
    """Format provided data in str anf cut length of provided data.

    Args:
        value: convert to str and cut.
        nested: id provided data is nested part of already provided value.
    """
    if isinstance(value, list):
        if (length := len(value)) > MIN_LENGTH_LIST:
            formatted_list = value.copy()
            del formatted_list[MIN_LENGTH_LIST:]
            if not nested:
                formatted_list.append(f"several items were not printed {length - MIN_LENGTH_LIST}")

            return [make_it_short(item) for item in formatted_list]
        return [make_it_short(item) for item in value]

    if isinstance(value, tuple):
        if (length := len(value)) > MIN_LENGTH_LIST:
            formatted_list = list(value).copy()
            del formatted_list[MIN_LENGTH_LIST:]
            if not nested:
                formatted_list.append(f"several items were not printed {length - MIN_LENGTH_LIST}")

            return tuple(make_it_short(item) for item in formatted_list)
        return tuple(make_it_short(item) for item in value)

    if isinstance(value, dict):
        if (length := len(value)) > MIN_LENGTH_DICT:
            return _dict_processing(value, nested, length)
        return {key: make_it_short(value[key]) for key in value}

    if is_dataclass(value):
        return make_it_short(asdict(value))

    if isinstance(value, str):
        max_size = MIN_LENGTH_STR // 5
        if (length := len(value)) > MIN_LENGTH_STR:
            formatted_str = []
            i = 0
            for k in range(max_size, length, max_size):
                formatted_str.append(value[i:k])
                i += max_size
            formatted_data = make_it_short(formatted_str, nested=True)
            return f'{"".join(formatted_data)} ...'
        return value

    return value


# TODO Rename this here and in `make_it_short`
def _dict_processing(value, nested, length):
    formatted_data = value.copy()
    keys = list(value.keys())
    del keys[:MIN_LENGTH_DICT]
    for key in keys:
        del formatted_data[key]

    formatted_data = {key: make_it_short(formatted_data[key]) for key in formatted_data}

    return (
        formatted_data
        if nested
        else [
            formatted_data,
            f"several items were not printed {length - MIN_LENGTH_DICT}",
        ]
    )
