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


# FOR ERRORS
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


# TOKENS

# Data types
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_STRING = "STRING"

# Identifiers, Keywords, Reswords
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_KEYWORD = "KEYWORD"
TOKEN_RESWORD = "RESERVED WORD"

# Arithmetic
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MUL = "MULTIPLY"
TOKEN_POW = "POWER"
TOKEN_DIV = "DIVIDE"
TOKEN_FLRDIV = "FLOOR DIVISION"
TOKEN_MOD = "MODULO"

# Assignment
TOKEN_ASSIGN = "ASSIGNMENT"

# Comparison
TOKEN_EQ = "EQUALS"
TOKEN_NEQ = "NOT EQUALS"
TOKEN_LT = "LESS THAN"
TOKEN_LTE = "LESS THAN / EQUALS"
TOKEN_GT = "GREATER THAN"
TOKEN_GTE = "GREATER THAN / EQUALS"

# Delimeters
TOKEN_LPAREN = "LEFT PARENTHESIS"
TOKEN_RPAREN = "RIGHT PARENTHESIS"
TOKEN_LBRACKET = "LEFT BRACKET"
TOKEN_RBRACKET = "RIGHT BRACKET"
TOKEN_LBRACE = "LEFT BRACE"
TOKEN_RBRACE = "RIGHT BRACE"
TOKEN_SEMI = "SEMICOLON"
TOKEN_COMMA = "COMMA"

# Unsure
TOKEN_NEWLINE = "NEWLINE"


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
                self.advance()

            # Identifiers, Keywords, Reserved words
            elif self.current_char in LETTERS:
                tokens.append(self.tokenize_word())
                self.advance()

            # Strings
            elif self.current_char == '"':
                tokens.append(self.make_string())

            ####################### COMBINE INTO ONE FUNCTION ###########################
            # Arithmetic
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_PLUS))
                self.advance()

            elif self.current_char == "-":
                tokens.append(Token(TOKEN_MINUS))
                self.advance()

            elif self.current_char == "*":
                tokens.append(self.tokenize_mul_or_pow())

            elif self.current_char == "/":
                tokens.append(self.tokenize_div())

            elif self.current_char == "%":
                tokens.append(Token(TOKEN_MOD))
                self.advance()

            # Comparison
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)

            elif self.current_char == "=":
                tokens.append(self.make_equals())

            elif self.current_char == "<":
                tokens.append(self.make_less_than())

            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            ########################### END OF REFACTOR #############################

            # Delimiters
            elif self.current_char == "(":
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()

            elif self.current_char == ")":
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()

            elif self.current_char == "[":
                tokens.append(Token(TOKEN_LBRACKET))
                self.advance()

            elif self.current_char == "]":
                tokens.append(Token(TOKEN_RBRACKET))
                self.advance()

            elif self.current_char == "{":
                tokens.append(Token(TOKEN_LBRACE))
                self.advance()

            elif self.current_char == "}":
                tokens.append(Token(TOKEN_RBRACE))
                self.advance()

            elif self.current_char == ";":
                tokens.append(Token(TOKEN_SEMI))
                self.advance()

            elif self.current_char == ",":
                tokens.append(Token(TOKEN_COMMA))
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
            return Token(TOKEN_FLOAT, float(num))
        return Token(TOKEN_INT, int(num))

    def tokenize_word(self):
        word = ""

        while (self.current_char is not None) and (self.current_char in ALPHANUMERIC + "_"):
            word += self.current_char
            self.advance()

        if word in RESERVED_WORDS:
            return Token(TOKEN_RESWORD, word)
        if word in KEYWORDS:
            return Token(TOKEN_KEYWORD, word)
        return Token(TOKEN_IDENTIFIER, word)

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
        return Token(TOKEN_STRING, f'"{str}"')

    # combine into one function
    def make_not_equals(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TOKEN_NEQ), None

    def make_equals(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TOKEN_EQ)

        return Token(TOKEN_ASSIGN)

    def make_less_than(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TOKEN_LTE)

        return Token(TOKEN_LT)

    def make_greater_than(self):
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TOKEN_GTE)

        return Token(TOKEN_GT)

    def tokenize_div(self):
        self.advance()

        if self.current_char == "/":
            self.advance()
            return Token(TOKEN_FLRDIV)

        return Token(TOKEN_DIV)

    def tokenize_mul_or_pow(self):
        self.advance()

        if self.current_char == "*":
            self.advance()
            return Token(TOKEN_POW)

        return Token(TOKEN_MUL)
    # end of code for combined function

# RUN


def run(file, text):
    lexer = Lexer(file, text)
    tokens, error = lexer.tokenize()

    return tokens, error
