"""JSON lexer."""
# pylint: disable=line-too-long, implicit-str-concat
# missing-module-docstring # noqa: D104,E501,D100,D101,D102
from pygments import unistring as uni
from pygments.lexer import (
    RegexLexer,
    bygroups,
    combined,
    include,
)
from pygments.token import (
    Comment,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Token,
)

CustomTrue = Token.CustomTrue
CustomFalse = Token.CustomFalse
CustomNull = Token.Null
FormatSeparator = Token.FormatSeparator
SpecialMessages = Token.SpecialMessages
Table_1 = Token.Table_1
Table_Header = Token.Header


def innerstring_rules(ttype):  # TODO: Optimize
    """Rules for inner(nested) strings."""
    return [
        (
            r"%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?" "[hlL]?[E-GXc-giorsaux%]",
            String.Interpol,
        ),
        (
            r"\{"
            r"((\w+)((\.\w+)|(\[[^\]]+\]))*)?"  # field name
            r"(\![sra])?"  # conversion
            r"(\:(.?[<>=\^])?[-+ ]?#?0?(\d+)?,?(\.\d+)?[E-GXb-gnosx%]?)?"
            r"\}",
            String.Interpol,
        ),
        (r'[^\\\'"%{\n]+', ttype),
        (r'[\'"\\]', ttype),
        (r"%|(\{{1,2})", ttype),
    ]


class JSONPythonLexer(RegexLexer):
    """Lexer."""

    name = "JSONPython"

    uni_name = f"[{uni.xid_start}][{uni.xid_continue}]*"

    # flags = re.MULTILINE | re.UNICODE

    tokens = {
        "root": [
            (r"(?<=\|\|)([a-zA-Z1-9 _]*)(?=\|\|)", Table_Header),
            (r"\n", Text),
            (r'^(\s*)([rRuUbB]{,2})("""(?:.|\n)*?""")', bygroups(Text, String.Affix, String.Doc)),
            (r"^(\s*)([rRuUbB]{,2})('''(?:.|\n)*?''')", bygroups(Text, String.Affix, String.Doc)),
            (r"\A#!.+$", Comment.Hashbang),
            (r"#.*$", Comment.Single),
            (r"\\\n", Text),
            (r"\\", Text),
            # (r'(def)((?:\s|\\\s)+)', bygroups(Keyword, Text), 'funcname'),
            # (r'(class)((?:\s|\\\s)+)', bygroups(Keyword, Text), 'classname'),
            (r"several items were not printed", SpecialMessages),
            (r"True|true", CustomTrue),
            (r"False|false", CustomFalse),
            (r"None|none", CustomNull),
            #
            (r"[1-9]+[a-z]", Text.Addition_2),
            (r"[?!]", Text.Addition_3),
            (r"(?<=\n\t.)\+(?=[a-zA-Z1-9])", FormatSeparator),
            (r"[╒═╤╕╞╪╡├─┼┤╘╧╛│]", Table_1),
            include("expr"),
        ],
        "expr": [
            # raw f-strings
            # ('(?i)(rf|fr)(""")', bygroups(String.Affix, String.Double), combined("rfstringescape", "tdqf")),
            # ("(?i)(rf|fr)(''')", bygroups(String.Affix, String.Single), combined("rfstringescape", "tsqf")),
            ('(?i)(rf|fr)(")', bygroups(String.Affix, String.Double), combined("rfstringescape", "dqf")),
            ("(?i)(rf|fr)(')", bygroups(String.Affix, String.Single), combined("rfstringescape", "sqf")),
            # non-raw f-strings
            # ('([fF])(""")', bygroups(String.Affix, String.Double), combined("fstringescape", "tdqf")),
            # ("([fF])(''')", bygroups(String.Affix, String.Single), combined("fstringescape", "tsqf")),
            ('([fF])(")', bygroups(String.Affix, String.Double), combined("fstringescape", "dqf")),
            ("([fF])(')", bygroups(String.Affix, String.Single), combined("fstringescape", "sqf")),
            # raw strings
            # ('(?i)(rb|br|r)(""")', bygroups(String.Affix, String.Double), "tdqs"),
            # ("(?i)(rb|br|r)(''')", bygroups(String.Affix, String.Single), "tsqs"),
            ('(?i)(rb|br|r)(")', bygroups(String.Affix, String.Double), "dqs"),
            ("(?i)(rb|br|r)(')", bygroups(String.Affix, String.Single), "sqs"),
            # non-raw strings
            # ('([uUbB]?)(""")', bygroups(String.Affix, String.Double), combined("stringescape", "tdqs")),
            # ("([uUbB]?)(''')", bygroups(String.Affix, String.Single), combined("stringescape", "tsqs")),
            ('([uUbB]?)(")', bygroups(String.Affix, String.Double), combined("stringescape", "dqs")),
            ("([uUbB]?)(')", bygroups(String.Affix, String.Single), combined("stringescape", "sqs")),
            include("numbers"),
            (r"[^\S\n]+", Text),
            (r"!=|==|<<|>>|:=|[-~+/*%=<>&^|.]", Operator),
            (r"[]{}:(),;[]", Punctuation),
            # (r'(in|is|and|or|not)\b', Operator.Word),
            include("name"),
        ],
        "numbers": [
            (r"(\d(?:_?\d)*\.(?:\d(?:_?\d)*)?|(?:\d(?:_?\d)*)?\.\d(?:_?\d)*)" r"([eE][+-]?\d(?:_?\d)*)?", Number.Float),
            (r"\d(?:_?\d)*[eE][+-]?\d(?:_?\d)*j?", Number.Float),
            (r"0[oO](?:_?[0-7])+", Number.Oct),
            (r"0[bB](?:_?[01])+", Number.Bin),
            (r"0[xX](?:_?[a-fA-F0-9])+", Number.Hex),
            (r"\d(?:_?\d)*", Number.Integer),
        ],
        "name": [
            (r"@" + uni_name, Name.Decorator),
            (r"@", Operator),  # new matrix multiplication operator
            (uni_name, Name),
        ],
        "rfstringescape": [
            (r"\{\{", String.Escape),
            (r"\}\}", String.Escape),
        ],
        "fstringescape": [
            include("rfstringescape"),
            include("stringescape"),
        ],
        "stringescape": [
            (
                r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|' r"U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})",
                String.Escape,
            )
        ],
        "strings-single": innerstring_rules(String.Single),
        "strings-double": innerstring_rules(String.Double),
        "dqf": [
            (r'"', String.Double, "#pop"),
            (r'\\\\|\\"|\\\n', String.Escape),  # included here for raw strings
        ],
        "sqf": [
            (r"'", String.Single, "#pop"),
            (r"\\\\|\\'|\\\n", String.Escape),  # included here for raw strings
        ],
        "dqs": [
            (r'"', String.Double, "#pop"),
            (r'"', String.Double, "#pop"),
            (r'\\\\|\\"|\\\n', String.Escape),  # included here for raw strings
            include("strings-double"),
        ],
        "sqs": [
            (r"'", String.Single, "#pop"),
            (r"\\\\|\\'|\\\n", String.Escape),  # included here for raw strings
            include("strings-single"),
        ],
    }


JSONLexer = JSONPythonLexer
