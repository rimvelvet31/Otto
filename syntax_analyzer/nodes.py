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
        if self.op_token.value == "not":
            return f"({self.op_token.value} {self.node})"
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
        condition_str = f"if ({self.cases[0][0]}) " + "{\n"
        for stmt in self.cases[0][1]:
            condition_str += f"\t{stmt}\n"
        condition_str += "}\n"

        for condition, stmts in self.cases[1:]:
            condition_str += f"elif ({condition}) " + "{\n"
            for stmt in stmts:
                condition_str += f"\t{stmt}\n"
            condition_str += "}\n"

        condition_str += "else " + "{\n"
        for stmt in self.else_case:
            condition_str += f"\t{stmt}\n"
        condition_str += "}\n"

        return condition_str


class ForStmtNode:
    def __init__(self, loop_var, arr, body):
        self.loop_var = loop_var
        self.arr = arr
        self.body = body

    def __repr__(self):
        for_str = f"for {self.loop_var.value} in {self.arr.value} " + "{\n"
        for stmt in self.body:
            for_str += f"\t{stmt}\n"
        for_str += "}"

        return for_str


class WhileStmtNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        while_str = f"while ({self.condition})" + "{\n"
        for stmt in self.body:
            while_str += f"\t{stmt}\n"
        while_str += "}"

        return while_str


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
        test_str = "test " + "{\n"
        for case in self.cases:
            test_str += f"\t{case}\n"
        test_str += "}"

        return test_str


class ExecuteStmtNode:
    def __init__(self, arr, func):
        self.arr = arr
        self.func = func

    def __repr__(self):
        return f"execute({self.arr}, {self.func});"


class FunctionCallNode:
    def __init__(self, atom, args):
        self.atom = atom
        self.args = args

    def __repr__(self):
        return f"{self.atom}({", ".join([str(arg) for arg in self.args])})"
