from lexer.constants import *
from lexer.regex import *
from lexer.position import Position


class Token:
    def __init__(self, type_, value, start_pos, end_pos=None):
        self.type = type_
        self.value = value

        if start_pos:
            self.start_pos = start_pos.copy()

            # end_pos is not provided
            self.end_pos = start_pos.copy()
            self.end_pos.advance()

        # end_pos is provided
        if end_pos:
            self.end_pos = end_pos.copy()

    def matches(self, type, value=None):
        return self.type == type and self.value == value

    def __repr__(self):
        return f"{self.type}:{self.value}"


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
            elif self.current_char.isdigit():
                tokens.append(self.make_num())

            # Tokenize operators
            elif self.current_char in VALID_OPERATOR_CHARS:
                tokens.append(self.make_operator(self.current_char))

            # Identifiers, Keywords, Reserved words, Noise words
            elif self.current_char.isalpha():
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
                tokens.append(self.make_delim())

            # Invalid char
            else:
                tokens.append(self.make_invalid(self.pos))

        # Indicates end of file
        tokens.append(Token("EOF", "EOF", start_pos=self.pos))
        return tokens

    # Helper methods
    def make_num(self):
        start_pos = self.pos.copy()

        num = ""

        while (self.current_char is not None) and (self.current_char in DIGITS + "."):
            num += self.current_char
            self.advance()

        # This is when a number is used to start an identifier
        if self.current_char is not None and self.current_char in LETTERS:
            return self.make_invalid(start_pos, num)

        if match_float(num):
            return Token("FLOAT", num, start_pos, self.pos)

        if match_int(num):
            return Token("INT", num, start_pos, self.pos)

        return self.make_invalid(start_pos, num)

    def make_word(self):
        start_pos = self.pos.copy()

        word = ""

        while (self.current_char is not None) and self.current_char in VALID_IDENTIFIER_CHARS:
            word += self.current_char
            self.advance()

        if self.current_char not in VALID_IDENTIFIER_CHARS and self.current_char not in DELIMITERS and not self.current_char.isspace():
            return self.make_invalid(start_pos, word)

        if word in WORD_OPERATORS:
            return Token(WORD_OPERATORS[word], word, start_pos, self.pos)

        if word in RESWORDS:
            return Token("RESWORD", word, start_pos, self.pos)

        if word in KEYWORDS:
            return Token("KEYWORD", word, start_pos, self.pos)

        if word in NOISE_WORDS:
            word_table = {
                "delete": ["del", "ete"],
                "except": ["exc", "ept"],
                "finally": ["final", "ly"],
            }

            keyword = word_table[word][0]
            noise_word = word_table[word][1]

            return [
                Token("KEYWORD", keyword, start_pos, self.pos),
                Token("NOISE_WORD", noise_word, start_pos, self.pos)
            ]

        if IDENTIFIER_REGEX.match(word):
            return Token("IDENTIFIER", word, start_pos, self.pos)

        return self.make_invalid(start_pos, word)

    def make_string(self, quote):
        start_pos = self.pos.copy()

        escape_chars = {
            "n": "\n",  # newline
            "t": "\t",  # tab
            "r": "\r",  # carriage return
        }

        str = ""
        escape_char = False
        self.advance()

        while (self.current_char is not None) and (self.current_char != quote or escape_char):
            if escape_char:
                str += escape_chars.get(self.current_char, self.current_char)
                escape_char = False
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    str += self.current_char
            self.advance()

        # Raise error if string is not properly terminated
        if self.current_char != quote:
            return Token("UNCLOSED_STR", f'"{str}', start_pos, self.pos)

        self.advance()  # Consume closing quote

        str_with_quotes = f'"{str}"' if quote == '"' else f"'{str}'"

        # Checks if the next char is a letter (identifiers cannot start with strings)
        if self.current_char is not None and self.current_char in LETTERS:
            return self.make_invalid(start_pos, str_with_quotes)

        return Token("STRING", str_with_quotes, start_pos, self.pos)

    def make_operator(self, operator):
        start_pos = self.pos.copy()

        operator_type = operator
        self.advance()

        # If current char is just "!", it should return an invalid token
        if operator == "!" and self.current_char != "=":
            return self.make_invalid(start_pos)

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
            return self.make_invalid(start_pos, operator_type)

        return Token(token, operator_type, start_pos, self.pos)

    def make_comment(self):
        start_pos = self.pos.copy()

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

            return Token("ML_COMMENT", comment_text, start_pos, self.pos)

        # Single-line comment
        while (self.current_char is not None) and (self.current_char != "\n"):
            comment_text += self.current_char
            self.advance()

        return Token("SL_COMMENT", comment_text, start_pos, self.pos)

    def make_delim(self):
        start_pos = self.pos.copy()

        delim_char = self.current_char
        delim_type = DELIMITERS.get(delim_char)
        self.advance()

        return Token(delim_type, delim_char, start_pos, self.pos)

    def make_invalid(self, start_pos, text=""):
        # if not start_pos:
        #     start_pos = self.pos.copy()

        while (self.current_char is not None) and (not self.current_char.isspace()):
            text += self.current_char
            self.advance()

        return Token("INVALID_TOKEN", text, start_pos, self.pos)

    def peek(self, offset=1):
        peek_idx = self.pos.idx + offset
        return self.text[peek_idx] if peek_idx < len(self.text) else None


# RUN
def run(file, text):
    lexer = Lexer(file, text)
    tokens = lexer.tokenize()

    return tokens
