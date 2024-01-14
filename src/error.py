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


class UnterminatedStrError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Unterminated String", details)
