import string

# CONSTANTS
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

RESERVED_WORDS = [
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


# ERROR HANDLING
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def error_message(self):
        message = f"{self.error_name}: {self.details}\n"
        message += f"File {self.pos_start.file_name}, line {self.pos_start.ln + 1}"
        return message


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


# POSITION
class Position:
    def __init__(self, idx, ln, col, file_name, file_text):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.file_text)


# TOKEN
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


# LEXER
class Lexer:
    def __init__(self, file, text):
        self.file = file
        self.text = text
        self.pos = Position(-1, 0, -1, file, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def tokenize(self):
        tokens = []

        while self.current_char is not None:

            # Ignore spaces and tabs
            if self.current_char in " \t":
                self.advance()

            # Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.tokenize_num())

            # Identifiers, Keywords, Reserved words
            elif self.current_char in LETTERS:
                tokens.append(self.tokenize_word())

            # Tokenize strings
            elif self.current_char == '"':
                tokens.append(self.make_string())

            # Tokenize operators
            elif self.current_char in "+-*/%=<>=!":
                tokens.append(self.make_operator(self.current_char))

            # Tokenize delimiters
            elif self.current_char in DELIMITERS:
                token = DELIMITERS.get(self.current_char)
                tokens.append(Token(token, self.current_char))
                self.advance()

            # Invalid char
            else:
                err_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(err_start, self.pos, f"'{char}'")

        return tokens, None

    def tokenize_num(self):
        num = ""
        has_dot = False

        while (self.current_char is not None) and (self.current_char in DIGITS + "."):
            if self.current_char == ".":
                # if num already has decimal point
                if has_dot:
                    break
                has_dot = True
                num += "."
            else:
                num += self.current_char
            self.advance()

        if has_dot:
            return Token("FLOAT", num)
        return Token("INT", num)

    def tokenize_word(self):
        word = ""

        while (self.current_char is not None) and (self.current_char in ALPHANUMERIC + "_"):
            word += self.current_char
            self.advance()

        if word in RESERVED_WORDS:
            return Token("RESERVED WORD", word)
        if word in KEYWORDS:
            return Token("KEYWORD", word)
        return Token("IDENTIFIER", word)

    def make_string(self):
        escape_chars = {
            "n": "\n",
            "t": "\t"
        }

        str = ""
        escape_char = False
        self.advance()

        while (self.current_char is not None) and (self.current_char != '"' or escape_char):
            if escape_char:
                str += escape_chars.get(self.current_char, self.current_char)
                escape_char = False
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    str += self.current_char
            self.advance()

        # Check if string is properly terminated
        if self.current_char != '"':
            raise Exception("Unterminated String")

        self.advance()
        return Token("STRING", f'"{str}"')

    # handle operators
    def make_operator(self, operator):
        lexeme = operator
        self.advance()

        while (self.current_char is not None) and (self.current_char in "+-*/%=<>=!"):
            if operator == "*" and self.current_char == "*":
                lexeme += self.current_char
                self.advance()

            if operator == "/" and self.current_char == "/":
                lexeme += self.current_char
                self.advance()

            if self.current_char == "=":
                lexeme += self.current_char
                self.advance()

        token = OPERATORS.get(lexeme)
        return Token(token, lexeme)


# RUN
def run(file, text):
    lexer = Lexer(file, text)
    tokens, error = lexer.tokenize()

    return tokens, error
