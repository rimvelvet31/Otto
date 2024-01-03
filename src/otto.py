from src.constants import DIGITS, LETTERS, ALPHANUMERIC, KEYWORDS, RESWORDS, OPERATORS, DELIMITERS
from src.position import Position
from src.error import IllegalCharError


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


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
            elif self.current_char in LETTERS:
                tokens.append(self.make_word())

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

        while (self.current_char is not None) and (self.current_char in ALPHANUMERIC + "_"):
            word += self.current_char
            self.advance()

        if word in RESWORDS:
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
