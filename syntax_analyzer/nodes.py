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


class IdentifierNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


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


class AssignStmtNode:
    def __init__(self, identifier, op, value):
        self.identifier = identifier
        self.op = op
        self.value = value

    def __repr__(self):
        return f"{self.identifier.value} {self.op.value} {self.value};"


class InputStmtNode:
    def __init__(self, identifier, prompt):
        self.identifier = identifier
        self.prompt = prompt

    def __repr__(self):
        return f"{self.identifier.value} = input({self.prompt});"


class OutputStmtNode:
    def __init__(self, output):
        self.output = output

    def __repr__(self):
        return f"utter({self.output});"


class ConditionalStmtNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

    def __repr__(self):
        condition_str = f"if {self.cases[0][0]} : {self.cases[0][1]}\n"

        for condition, stmt in self.cases[1:]:
            condition_str += f"elif {condition} : {stmt}\n"

        condition_str += f"else : {self.else_case}" if self.else_case else ""

        return condition_str
