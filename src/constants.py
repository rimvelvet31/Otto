import re
import string

DIGITS = "0123456789"

LETTERS = string.ascii_letters

VALID_IDENTIFIER_CHARS = LETTERS + DIGITS + "_"

# IDENTIFIER RULES
# - Identifiers are case sensitive
# - They cannot contain whitespace
# - They cannot contain special chars, expect underscore (_)
# - They can contain numbers, but are not allowed to start with one
# - They must start with an uppercase or lowercase letter, or with underscore
IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

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

NOISE_WORDS = ["delete", "except", "finally"]

RESWORDS = ["true", "false", "null"]

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
