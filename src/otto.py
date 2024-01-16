from src.constants import *
from src.position import Position


class Token:
    def __init__(self, type_, value):
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
        # List of Token objects with attributes: type, value)
        tokens = []

        while self.current_char is not None:

            # Ignore spaces and tabs
            if self.current_char in " \t":
                self.advance()

            # Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.make_num())

            # Identifiers, Keywords, Reserved words, Noise words
            elif self.current_char in LETTERS + "_":
                word_token = self.make_word()

                # To handle noise words
                if isinstance(word_token, list):
                    keyword_token = word_token[0]
                    noise_word_token = word_token[1]

                    tokens.append(keyword_token)
                    tokens.append(noise_word_token)

                # For indentifiers, keywords, reswords
                else:
                    tokens.append(word_token)

            # Tokenize strings
            elif self.current_char in ("'", '"'):
                tokens.append(self.make_string(self.current_char))

            # Tokenize operators
            elif self.current_char in VALID_OPERATOR_CHARS:
                tokens.append(self.make_operator(self.current_char))

            # Tokenize comments
            elif self.current_char == "#":
                tokens.append(self.make_comment())

            # Tokenize delimiters
            elif self.current_char in DELIMITERS:
                token = DELIMITERS.get(self.current_char)
                tokens.append(Token(token, self.current_char))
                self.advance()

            # Invalid char
            else:
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

        while self.current_char is not None and self.current_char in VALID_IDENTIFIER_CHARS:
            word += self.current_char
            self.advance()

        if word in WORD_OPERATORS:
            return Token(WORD_OPERATORS[word], word)

        if word in RESWORDS:
            return Token("RESERVED WORD", word)

        if word in KEYWORDS:
            return Token("KEYWORD", word)

        if word in NOISE_WORDS:
            word_table = {
                "delete": ["del", "ete"],
                "except": ["exc", "ept"],
                "finally": ["final", "ly"],
            }

            keyword = word_table[word][0]
            noise_word = word_table[word][1]

            return [Token("KEYWORD", keyword), Token("NOISE WORD", noise_word)]

        if IDENTIFIER_REGEX.match(word):
            return Token("IDENTIFIER", word)

        return Token("INVALID", word)

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

            # Equality / Compound assignment
            if self.current_char == "=":
                lexeme += self.current_char
                self.advance()

        token = SYMBOL_OPERATORS.get(lexeme)
        return Token(token, lexeme)

    def make_comment(self):
        comment_text = self.current_char
        self.advance()  # Consume the "#"

        # Treat everything after the "#" but before a newline as a comment
        while (self.current_char is not None) and (self.current_char != "\n"):
            comment_text += self.current_char
            self.advance()
        return Token("COMMENT", comment_text)


# TODO Move scanning logic from tokenize to here and put this on the diff file
def run(file, text):
    lexer = Lexer(file, text)
    tokens = lexer.tokenize()

    return tokens
