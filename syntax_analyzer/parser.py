from syntax_analyzer.nodes import *
from utils.error import InvalidSyntaxError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.read_token()

    def read_token(self):
        self.token_idx += 1

        # Check if token index is within bounds
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]

        return self.current_token

    def next_token(self):
        next_idx = self.token_idx + 1
        if next_idx < len(self.tokens):
            return self.tokens[next_idx].type
        else:
            return None

    # Entry point of parser
    def otto_progstmt(self):
        # TODO add support for multiple statements
        res = self.stmt()

        # Check if res was returned even when are still unparsed tokens
        # if self.current_token.type != "EOF":
        #     return InvalidSyntaxError(
        #         self.current_token.start_pos,
        #         self.current_token.end_pos,
        #         "Expected arithmetic or boolean operator"
        #     )

        return res

    # Statements
    def stmt(self):

        # Parse either assignment or input statement
        if self.current_token.type == "IDENTIFIER":

            # If next token is "=", go to either input or assignment statement
            if self.next_token() == "ASSIGN_OP":
                # Read the identifier token
                identifier = self.current_token
                self.read_token()

                # Read the assignment operator
                op = self.current_token
                self.read_token()

                # Parse as input statement if "input" keyword is found
                if self.current_token.matches("KEYWORD", "input"):
                    return self.input_stmt(identifier)

                # Otherwise, parse as assignment statement
                return self.assign_stmt(identifier, op)

            # For compound assignment expressions
            compound_assign_ops = ("ADD_ASSIGN_OP", "SUB_ASSIGN_OP", "MUL_ASSIGN_OP",
                                   "DIV_ASSIGN_OP", "FDIV_ASSIGN_OP", "MOD_ASSIGN_OP",
                                   "POW_ASSIGN_OP")

            if self.next_token() in compound_assign_ops:
                # Read the identifier token
                identifier = self.current_token
                self.read_token()

                # Read the compound assignment operator
                op = self.current_token
                self.read_token()

                # Parse as assignment statement
                return self.assign_stmt(identifier, op)

        # Parse output statement
        elif self.current_token.matches("KEYWORD", "utter"):
            return self.output_stmt()

        # Parse conditional statement
        elif self.current_token.matches("KEYWORD", "if"):
            return self.conditional_stmt()

        # Parse iterative statements
        elif self.current_token.matches("KEYWORD", "for"):
            pass

        elif self.current_token.matches("KEYWORD", "while"):
            pass

        # Parse arithmetic and/or boolean expressions
        expr = self.logical_expr()

        # Check if expression ends with semicolon
        if self.current_token.type != "SEMI_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ';'"
            )
        self.read_token()

        return expr

    # Statement Methods
    def assign_stmt(self, identifier, op):
        value = self.logical_expr()

        # Check if statement ends with semicolon
        if self.current_token.type != "SEMI_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ';'"
            )
        self.read_token()

        return AssignStmtNode(identifier, op, value)

    def input_stmt(self, identifier):
        # Read "input" keyword
        self.read_token()

        # Check if next token is "("
        if self.current_token.type != "LPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '('"
            )
        self.read_token()

        # Parse input prompt (string or identifier)
        prompt = self.atom()

        # Check if next token is ")"
        if self.current_token.type != "RPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ')'"
            )
        self.read_token()

        # Check if statement ends with semicolon
        if self.current_token.type != "SEMI_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ';'"
            )
        self.read_token()

        return InputStmtNode(identifier, prompt)

    def output_stmt(self):
        # Read "utter" keyword
        self.read_token()

        # Check if next token is "("
        if self.current_token.type != "LPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '('"
            )
        self.read_token()

        # Parse output value
        output = self.logical_expr()

        # Check if next token is ")"
        if self.current_token.type != "RPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ')'"
            )
        self.read_token()

        # Check if statement ends with semicolon
        if self.current_token.type != "SEMI_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ';'"
            )
        self.read_token()

        return OutputStmtNode(output)

    def conditional_stmt(self):
        # Stores each if/elif's condition & body
        cases = []
        else_case = None

        # Read "if" keyword
        self.read_token()

        # Parse if condition and body
        if_condition = self.condition_check()
        if_body = self.code_block()
        cases.append((if_condition, if_body))

        # Parse elif conditions and bodies
        while self.current_token.matches("KEYWORD", "elif"):
            # Read "elif" keyword
            self.read_token()

            # Parse elif condition and body
            elif_condition = self.condition_check()
            elif_body = self.code_block()
            cases.append((elif_condition, elif_body))

        # Parse else body
        if self.current_token.matches("KEYWORD", "else"):
            # Read "else" keyword
            self.read_token()

            # Parse else body
            else_case = self.code_block()

        return ConditionalStmtNode(cases, else_case)

    # Iterative statements
    def for_stmt(self):
        pass

    def while_stmt(self):
        pass

    # New Features
    def uniq_stmt(self):
        # Ottomate

        # Step

        # test

        # execute
        pass

    # OPERATIONS (lowest to highest precedence: logical_expr -> atom)
    # Boolean expressions
    def logical_expr(self):
        return self.binary_op(self.comparison_expr, ("AND_OP", "OR_OP"))

    def comparison_expr(self):
        # not
        if self.current_token.type == "NOT_OP":
            not_token = self.current_token
            self.read_token()

            node = self.comparison_expr()

            return UnaryOpNode(not_token, node)

        # Comparison operators
        comparison_ops = ("LT_OP", "GT_OP", "LTE_OP",
                          "GTE_OP", "EQ_OP", "NEQ_OP")
        return self.binary_op(self.add_subract, comparison_ops)

    # Arithmetic expressions
    def add_subract(self):
        return self.binary_op(self.modulo_multiply_divide, ("ADD_OP", "SUB_OP"))

    def modulo_multiply_divide(self):
        return self.binary_op(self.factor, ("MOD_OP", "MUL_OP", "DIV_OP", "FDIV_OP"))

    # For unary operation or exponentiation
    def factor(self):
        # Parse unary operations (positive or negative nums)
        token = self.current_token
        if token.type in ("ADD_OP", "SUB_OP"):
            self.read_token()
            factor = self.factor()
            return UnaryOpNode(token, factor)

        # For exponentiation
        return self.power()

    def power(self):
        return self.binary_op(self.atom, ("POW_OP",), self.factor)

    # Literals and parenthesis expressions
    def atom(self):
        token = self.current_token

        # Parse numbers
        if token.type in ("INT", "FLOAT"):
            self.read_token()
            return NumberNode(token)

        # Parse strings
        elif token.type == "STRING":
            self.read_token()
            return StringNode(token)

        # Parse identifiers
        elif token.type == "IDENTIFIER":
            self.read_token()
            return IdentifierNode(token)

        # Parse parenthesis expressions
        elif token.type == "LPAREN_DELIM":
            self.read_token()

            # Get expression inside parenthesis
            expr = self.logical_expr()

            # Check if parenthesis is closed
            if self.current_token.type != "RPAREN_DELIM":
                return InvalidSyntaxError(
                    self.current_token.start_pos,
                    self.current_token.end_pos,
                    "Expected ')'"
                )
            self.read_token()

            return expr

        # If none of the above, return error
        return InvalidSyntaxError(
            token.start_pos,
            token.end_pos,
            "Expected a value"
        )

    # HELPER METHODS
    def binary_op(self, left_nonterminal, accepted_ops, right_nonterminal=None):
        # Both left and right nonterminals are the same
        if right_nonterminal is None:
            right_nonterminal = left_nonterminal

        left_node = left_nonterminal()

        while self.current_token.type in accepted_ops:
            op_token = self.current_token
            self.read_token()

            # Recursively get the following operands
            right_node = right_nonterminal()

            left_node = BinaryOpNode(left_node, op_token, right_node)

        return left_node

    def condition_check(self):
        # Check if next token is "("
        if self.current_token.type != "LPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '('"
            )
        self.read_token()

        # Parse condition expression
        condition = self.logical_expr()

        # Check if next token is ")"
        if self.current_token.type != "RPAREN_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ')'"
            )
        self.read_token()

        return condition

    def code_block(self):
        # Check if next token is "{"
        if self.current_token.type != "LBRACE_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '{'"
            )
        self.read_token()

        # Get block body
        body = self.stmt()

        # Check if next token is "}"
        if self.current_token.type != "RBRACE_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '}'"
            )
        self.read_token()

        return body
