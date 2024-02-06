class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class StringNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class ListNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"{self.elements}"


class IdentifierNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class AssignStmtNode:
    def __init__(self, identifier_tok, value_node):
        self.identifier_tok = identifier_tok
        self.value_node = self.value_node = self.value_node = value_node

    def __repr__(self):
        return f"{self.identifier_tok.value} = {self.value_node};"


class BinaryOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node} {self.op_token.value} {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f"({self.op_token.value}{self.node})"


class ConditionStmtNode:
    def __init__(self, if_case, elif_cases, else_body):
        self.if_case = if_case
        self.elif_cases = elif_cases
        self.else_body = else_body

    def __repr__(self):
        return f"if {self.if_case} elif {self.elif_cases} else {self.else_body}"


class ForStmtNode:
    pass


class WhileStmtNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while {self.condition} {self.body}"


class InputStmtNode:
    def __init__(self, identifier, prompt):
        self.identifier = identifier
        self.prompt = prompt

    def __repr__(self):
        return f"{self.identifier.value} = input({self.prompt});"


class OutputStmtNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"utter({self.value});"
