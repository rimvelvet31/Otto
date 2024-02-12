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


class BoolNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class NullNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class IdentifierNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"


class ListNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"[{', '.join([str(element) for element in self.elements])}]"


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
        condition_str = f"if {self.cases[0][0]}:\n\t{self.cases[0][1]}\n"

        for condition, stmt in self.cases[1:]:
            condition_str += f"elif {condition}:\n\t{stmt}\n"

        condition_str += f"else:\n\t{
            self.else_case}" if self.else_case else ""

        return condition_str


class ForStmtNode:
    def __init__(self, loop_var, arr, body):
        self.loop_var = loop_var
        self.arr = arr
        self.body = body

    def __repr__(self):
        return f"for {self.loop_var} in {self.arr}"


class WhileStmtNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while ({self.condition}):\n\t{self.body}"


class OttomateStmtNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"Ottomate {self.identifier};"


class StepStmtNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"step {self.identifier};"


class TestStmtNode:
    def __init__(self, cases):
        self.cases = cases

    def __repr__(self):
        test_str = "test:"
        test_str += "\n\t".join([str(case) for case in self.cases])

        return test_str


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return "\n".join([str(statement) for statement in self.statements])


class CallNode:
    def __init__(self, atom, args):
        self.atom = atom
        self.args = args

    def __repr__(self):
        return f"{self.atom}({", ".join([str(arg) for arg in self.args])})"
