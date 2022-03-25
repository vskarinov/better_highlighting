import textwrap as tw
from typing import Union, Optional

MIN_LENGTH_STR = 250
MIN_LENGTH_LIST = 3
MIN_LENGTH_DICT = 10
MIN_LENGTH_STR_IN_DICT = 40


def pretty_as_iterator(value, htchar='\t', lfchar='\n', indent=0, key_length=0) -> str:
    tab_key_length = 4 if key_length != 0 else 0
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + pretty_as_iterator(value[key], htchar, lfchar, indent + 1,
                                                         key_length=len(str(key)))
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is list:
        items = [
            nlch + pretty_as_iterator(item, htchar, lfchar, indent + 1, key_length=0)
            for item in value
        ]
        return f"[{','.join(items) + lfchar + htchar * indent}]"
    elif type(value) is tuple:
        items = [
            nlch + pretty_as_iterator(item, htchar, lfchar, indent + 1, key_length=0)
            for item in value
        ]
        return f"({','.join(items) + lfchar + htchar * indent})"
    elif type(value) is str:
        w = MIN_LENGTH_STR_IN_DICT - (len(lfchar) + len(htchar) * (indent + (key_length + tab_key_length)))
        value = tw.wrap(value, width=w + 1)
        return f' {lfchar + htchar * (indent + key_length)}+'.join(value)
    elif type(value) is int:
        w = MIN_LENGTH_STR_IN_DICT - (len(lfchar) + len(htchar) * (indent + (key_length + tab_key_length)))
        value = tw.wrap(str(value), width=w + 1)
        return f' {lfchar + htchar * (indent + key_length)}+'.join(value)
    return repr(value)


def pretty_as_text(value) -> str:
    if type(value) is dict:
        items = [f'{repr(key)}: {pretty_as_text(value[key])}' for key in value]
        return '{%s}' % (', '.join(items))
    elif type(value) is list:
        items = [
            pretty_as_text(item)
            for item in value
        ]
        return f"[{', '.join(items)}]"
    elif type(value) is tuple:
        items = [
            pretty_as_text(item)
            for item in value
        ]
        return f"({', '.join(items)})"
    elif type(value) is str:
        value = tw.wrap(value)
        return f''.join(value)

    return repr(value)


def make_it_short(value: Union[str, list, dict], nested: Optional[bool] = False) -> Union[str, list, dict]:
    if type(value) is list:
        if (length := len(value)) > MIN_LENGTH_LIST:
            formatted_list = value.copy()
            del formatted_list[MIN_LENGTH_LIST:]
            if not nested:
                formatted_list.append(f'several items were not printed {length - MIN_LENGTH_LIST}')

            return [make_it_short(item) for item in formatted_list]
        return [make_it_short(item) for item in value]

    elif type(value) is dict:
        if (length := len(value)) > MIN_LENGTH_DICT:
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
                    f'several items were not printed {length - MIN_LENGTH_DICT}',
                ]
            )

        return {key: make_it_short(value[key]) for key in value}

    if type(value) is str:
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
