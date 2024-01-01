# CONSTANTS
DIGITS = "0123456789"


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

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.file_text)


# TOKENS
TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MUL = "MUL"
TOKEN_DIV = "DIV"
TOKEN_FLRDIV = "FLRDIV"
TOKEN_MODULO = "MODULO"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_EXPO = "EXPONENT"


class Token:
    def __init__(self, type, value=None):
        self.type = type
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

        while self.current_char != None:

            if self.current_char in " \t":
                self.advance()

            # Numbers
            elif self.current_char in DIGITS:
                tokens.append(self.tokenize_num())
                self.advance()

            # Operators
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_PLUS))
                self.advance()

            elif self.current_char == "-":
                tokens.append(Token(TOKEN_MINUS))
                self.advance()

            elif self.current_char == "*":
                tokens.append(Token(TOKEN_MUL))
                self.advance()

            elif self.current_char == "/":
                tokens.append(Token(TOKEN_DIV))
                self.advance()
            elif self.current_char == "%":
                tokens.append(Token(TOKEN_MODULO))
                self.advance()

            elif self.current_char == "(":
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()

            elif self.current_char == ")":
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()

            # Invalid char
            else:
                err_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(err_start, self.pos, f"'{char}'")

        return tokens, None

    def tokenize_num(self):
        num_str = ""
        has_dot = False

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if has_dot:
                    break
                has_dot = True
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if has_dot:
            return Token(TOKEN_FLOAT, float(num_str))
        else:
            return Token(TOKEN_INT, int(num_str))


# RUN
def run(file, text):
    lexer = Lexer(file, text)
    tokens, error = lexer.tokenize()

    return tokens, error
