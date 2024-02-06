from utils.error_squiggles import display_squiggles


class Error:
    def __init__(self, start_pos, end_pos, err_type, details):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.err_type = err_type
        self.details = details

    def __str__(self):
        message = f"{self.err_type}: {self.details}\n"
        message += f"File {self.start_pos.file_name}, line {self.start_pos.ln + 1}\n"
        message += "\n" + display_squiggles(
            self.start_pos.file_text, self.start_pos, self.end_pos
        )

        return message


# Lexer Errors
class IllegalCharError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, "Illegal Character", details)


class UnterminatedStrError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, "Unterminated String", details)


# Parser Errors
class InvalidSyntaxError(Error):
    def __init__(self, start_pos, end_pos, details=""):
        super().__init__(start_pos, end_pos, "Invalid Syntax", details)
