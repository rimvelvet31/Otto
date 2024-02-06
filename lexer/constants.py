import string

DIGITS = "0123456789"

LETTERS = string.ascii_letters + "_"

VALID_IDENTIFIER_CHARS = LETTERS + DIGITS

VALID_OPERATOR_CHARS = "+-*/%=!<>&|^~"

KEYWORDS = [
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
    "input"
    "lambda",
    "nonlocal",
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

SYMBOL_OPERATORS = {
    # Arithmetic
    "+": "ADD_OP",
    "-": "SUB_OP",
    "*": "MUL_OP",
    "/": "DIV_OP",
    "%": "MOD_OP",
    "**": "POW_OP",
    "//": "FDIV_OP",

    # Assignment
    "=": "ASSIGN_OP",
    "+=": "ADD_ASSIGN_OP",
    "-=": "SUB_ASSIGN_OP",
    "*=": "MUL_ASSIGN_OP",
    "/=": "DIV_ASSIGN_OP",
    "%=": "MOD_ASSIGN_OP",
    "**=": "POW_ASSIGN_OP",
    "//=": "FDIV_ASSIGN_OP",

    # Comparison
    ">": "LT_OP",
    "<": "GT_OP",
    ">=": "LTE_OP",
    "<=": "GTE_OP",
    "==": "EQ_OP",
    "!=": "NEQ_OP",

    # Bitwise
    "&": "BW_AND_OP",
    "|": "BW_OR_OP",
    "^": "BW_XOR_OP",
    "~": "BW_NOT_OP",
    "<<": "BW_LSHIFT_OP",
    ">>": "BW_RSHIFT_OP",
}

WORD_OPERATORS = {
    # Logical
    "and": "AND_OP",
    "or": "OR_OP",
    "not": "NOT_OP",

    # Identity
    "is": "IDENT_OP",

    # Membership
    "in": "MEMBER_OP",
}

DELIMITERS = {
    "(": "LPAREN_DELIM",
    ")": "RPAREN_DELIM",
    "[": "LBRACK_DELIM",
    "]": "RBRACK_DELIM",
    "{": "LBRACE_DELIM",
    "}": "RBRACE_DELIM",
    ";": "SEMI_DELIM",
    ",": "COMMA_DELIM"
}
