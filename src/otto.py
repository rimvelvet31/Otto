import re

from src.constants import *
from src.position import Position


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value


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
                tokens.append(self.make_num())

            # Identifiers, Keywords, Reserved words
            elif self.current_char in LETTERS + "_":
                tokens.append(self.make_word())

            # Tokenize strings
            elif self.current_char in ("'", '"'):
                tokens.append(self.make_string(self.current_char))

            # Tokenize operators
            elif self.current_char in VALID_OPERATOR_CHARS:
                tokens.append(self.make_operator(self.current_char))

            elif self.current_char == "#":
                tokens.append(self.make_comment())

            # Tokenize delimiters
            elif self.current_char in DELIMITERS:
                token = DELIMITERS.get(self.current_char)
                tokens.append(Token(token, self.current_char))
                self.advance()

            # Invalid char
            else:
                # err_start = self.pos.copy()
                # char = self.current_char
                # self.advance()
                # return [], IllegalCharError(err_start, self.pos, f"'{char}'")

                error_token = Token("INVALID", self.current_char)
                tokens.append(error_token)
                self.advance()

        return tokens

    # Helper methods
    def make_num(self):
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

    def make_word(self):
        word = ""

        # Identifier rules
        identifier_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

        while self.current_char is not None:
            word += self.current_char
            self.advance()

        if word in RESWORDS:
            return Token("RESERVED WORD", word)

        if word in KEYWORDS:
            return Token("KEYWORD", word)

        if not identifier_regex.match(word):
            return Token("INVALID", word)

        return Token("IDENTIFIER", word)

    def make_string(self, quote):
        escape_chars = {
            "n": "\n",
            "t": "\t"
        }

        strng = ""
        escape_char = False
        self.advance()

        while (self.current_char is not None) and (self.current_char != quote or escape_char):
            if escape_char:
                strng += escape_chars.get(self.current_char,
                                          self.current_char)
                escape_char = False
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    strng += self.current_char
            self.advance()

        # Raise error if string is not properly terminated
        if self.current_char != quote:
            return Token("UNTERMINATED STRING", f'"{strng}')

        self.advance()
        str_with_quotes = f'"{strng}"' if quote == '"' else f"'{strng}'"
        return Token("STRING", str_with_quotes)

    def make_operator(self, operator):
        lexeme = operator
        self.advance()

        # If current char is just "!", it should return an invalid token
        if operator == "!" and self.current_char != "=":
            return Token("INVALID", "!")

        while (self.current_char is not None) and (self.current_char in "+-*/%=<>&|^~"):
            # Exponent
            if operator == "*" and self.current_char == "*":
                lexeme += self.current_char
                self.advance()

            # Floor division
            if operator == "/" and self.current_char == "/":
                lexeme += self.current_char
                self.advance()

            # Bitwise left shift
            if operator == "<" and self.current_char == "<":
                lexeme += self.current_char
                self.advance()

            # Bitwise right shift
            if operator == ">" and self.current_char == ">":
                lexeme += self.current_char
                self.advance()

            if self.current_char == "=":
                lexeme += self.current_char
                self.advance()

        token = OPERATORS.get(lexeme)
        return Token(token, lexeme)

    def make_comment(self):
        comment_text = self.current_char
        self.advance()  # Consume opening "#"

        # TODO Multi-line comment

        # Single-line comment
        while (self.current_char is not None) and (self.current_char != "\n"):
            comment_text += self.current_char
            self.advance()
        return Token("SINGLE-LINE COMMENT", comment_text)

    def peek(self):
        if self.pos.idx + 1 < len(self.text):
            return self.text[self.pos.idx + 1]
        return None


# RUN
def run(file, text):
    lexer = Lexer(file, text)
    tokens = lexer.tokenize()

    return tokens
