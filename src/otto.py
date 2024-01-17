from src.constants import *
from src.regex import *
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

            # Ignore whitespace
            if self.current_char.isspace():
                self.advance()

            # Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.make_num())

            # Tokenize operators
            elif self.current_char in VALID_OPERATOR_CHARS:
                tokens.append(self.make_operator(self.current_char))

            # Identifiers, Keywords, Reserved words, Noise words
            elif self.current_char in LETTERS:
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
                tokens.append(self.make_invalid())

        return tokens

    # Helper methods

    def make_num(self):
        num = ""

        while (self.current_char is not None) and (self.current_char in DIGITS + "."):
            num += self.current_char
            self.advance()

        # Checks if the next char is a letter (identifiers cannot start with numbers)
        if self.current_char is not None and self.current_char in LETTERS:
            return self.make_invalid(num)

        if match_float(num):
            return Token("FLOAT", num)

        if match_int(num):
            return Token("INT", num)

        return self.make_invalid(num)

    def make_word(self):
        word = ""

        while (self.current_char is not None) and (self.current_char != " "):
            word += self.current_char
            self.advance()

        if word in WORD_OPERATORS:
            return Token(WORD_OPERATORS[word], word)

        if word in RESWORDS:
            return Token("RESWORD", word)

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

            return [Token("KEYWORD", keyword), Token("NOISE_WORD", noise_word)]

        if IDENTIFIER_REGEX.match(word):
            return Token("IDENTIFIER", word)

        return self.make_invalid(word)

    def make_string(self, quote):
        escape_chars = {
            "n": "\n",  # newline
            "t": "\t",  # tab
            "r": "\r",  # carriage return
        }

        strng = ""
        escape_char = False
        self.advance()

        while (self.current_char is not None) and (self.current_char != quote or escape_char):
            if escape_char:
                strng += escape_chars.get(self.current_char, self.current_char)
                escape_char = False
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    strng += self.current_char
            self.advance()

        # Raise error if string is not properly terminated
        if self.current_char != quote:
            return Token("UNCLOSED_STR", f'"{strng}')

        self.advance()  # Consume closing quote

        str_with_quotes = f'"{strng}"' if quote == '"' else f"'{strng}'"

        # Checks if the next char is a letter (identifiers cannot start with strings)
        if self.current_char is not None and self.current_char in LETTERS:
            return self.make_invalid(str_with_quotes)

        return Token("STRING", str_with_quotes)

    def make_operator(self, operator):
        operator_type = operator
        self.advance()

        # If current char is just "!", it should return an invalid token
        if operator == "!" and self.current_char != "=":
            return self.make_invalid()

        while (self.current_char is not None) and (self.current_char in "+-*/%=<>&|^~"):
            # Exponent
            if operator == "*" and self.current_char == "*":
                operator_type += self.current_char
                self.advance()

            # Floor division
            if operator == "/" and self.current_char == "/":
                operator_type += self.current_char
                self.advance()

            # Bitwise left shift
            if operator == "<" and self.current_char == "<":
                operator_type += self.current_char
                self.advance()

            # Bitwise right shift
            if operator == ">" and self.current_char == ">":
                operator_type += self.current_char
                self.advance()

            # Equality / Compound assignment
            if self.current_char == "=":
                operator_type += self.current_char
                self.advance()

        token = SYMBOL_OPERATORS.get(operator_type)

        # Checks if the next char is a letter (identifiers cannot start with special chars)
        if self.current_char is not None and self.current_char in LETTERS:
            return self.make_invalid(operator_type)

        return Token(token, operator_type)

    def make_comment(self):
        comment_text = self.current_char  # Consume opening "#"
        self.advance()

        # Multi-line comment
        if self.current_char == "*":
            comment_text += self.current_char  # Consume opening "*"
            self.advance()

            while self.current_char != "*" and self.peek() != "#":
                comment_text += self.current_char
                self.advance()

            # Consume closing "*#"
            for _ in range(2):
                comment_text += self.current_char
                self.advance()

            return Token("ML_COMMENT", comment_text)

        # Single-line comment
        while (self.current_char is not None) and (self.current_char != "\n"):
            comment_text += self.current_char
            self.advance()

        return Token("SL_COMMENT", comment_text)

    def make_invalid(self, text=""):
        while (self.current_char is not None) and (self.current_char != " "):
            text += self.current_char
            self.advance()

        return Token("INVALID_TOKEN", text)

    def peek(self, offset=1):
        peek_idx = self.pos.idx + offset
        return self.text[peek_idx] if peek_idx < len(self.text) else None


# RUN
def run(file, text):
    lexer = Lexer(file, text)
    tokens = lexer.tokenize()

    return tokens
