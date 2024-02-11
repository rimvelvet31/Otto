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
