import string

DIGITS = "0123456789"

LETTERS = string.ascii_letters

ALPHANUMERIC = DIGITS + LETTERS

KEYWORDS = [
    'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'collect',
    'continue', 'def', 'del', 'deliver', 'elif', 'else', 'except', 'finally',
    'for', 'from', 'global', 'if', 'import', 'in', 'lambda', 'nonlocal', 'not',
    'or', 'Ottomate', 'pass', 'pull', 'push', 'raise', 'retrieve', 'return',
    'scrub', 'step', 'try', 'while', 'with', 'yield'
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
