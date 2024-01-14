import string

DIGITS = "0123456789"

LETTERS = string.ascii_letters

VALID_IDENTIFIER_CHARS = LETTERS + DIGITS + "_"

VALID_OPERATOR_CHARS = "+-*/%=!<>&|^~"

KEYWORDS = [
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "check",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "exc",
    "execute",
    "final",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "input"
    "lambda",
    "nonlocal",
    "not",
    "or",
    "Ottomate",
    "pass",
    "raise",
    "return",
    "step",
    "test",
    "try",
    "utter",
    "while",
    "with",
    "yield"
]


RESWORDS = [
    "true", "false", "null"
]

OPERATORS = {
    # Arithmetic
    "+": "ADDITION",
    "-": "SUBTRACTION",
    "*": "MULTIPLICATION",
    "/": "DIVISION",
    "%": "MODULO",
    "**": "EXPONENT",
    "//": "FLOOR DIVISON",

    # Assignment
    "=": "ASSIGNMENT",
    "+=": "ADDITION ASSIGNMENT",
    "-=": "SUBTRACTION ASSIGNMENT",
    "*=": "MULTIPLICATION ASSIGNMENT",
    "/=": "DIVISION ASSIGNMENT",
    "%=": "MODULO ASSIGNMENT",
    "**=": "EXPONENT ASSIGNMENT",
    "//=": "FLOOR DIV ASSIGNMENT",

    # Comparison
    ">": "LESS THAN",
    "<": "GREATER THAN",
    ">=": "LESS THAN / EQUALS",
    "<=": "GREATER THAN / EQUALS",
    "==": "EQUALS",
    "!=": "NOT EQUALS",

    # Bitwise
    "&": "BITWISE AND",
    "|": "BITWISE OR",
    "^": "BITWISE XOR",
    "~": "BITWISE NOT",
    "<<": "BITWISE LEFT SHIFT",
    ">>": "BITWISE RIGHT SHIFT",
}

DELIMITERS = {
    "(": "LEFT PARENTHESIS",
    ")": "RIGHT PARENTHESIS",
    "[": "LEFT BRACKET",
    "]": "RIGHT BRACKET",
    "{": "LEFT BRACE",
    "}": "RIGHT BRACE",
    ";": "SEMICOLON",
    ",": "COMMA"
}
