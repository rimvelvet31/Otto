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
        if self.current_token.type != "EOF":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected arithmetic or boolean operator"
            )

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

        # For condition statements
        # if self.current_token.matches("KEYWORD", "if"):
        #     condition_stmt = res.register(self.condition_stmt())
        #     if res.error:
        #         return res
        #     return res.success(condition_stmt)

        # Parse iterative statements
        elif self.current_token.matches("KEYWORD", "for"):
            pass

        elif self.current_token.matches("KEYWORD", "while"):
            pass

        # For arithmetic or boolean expressions
        expr = self.expr()

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
        value = self.expr()

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
        output = self.expr()

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

    # Operations (lowest to highest precedence: expr -> atom)
    def expr(self):
        # For arithmetic expressions
        return self.add_subract()

        # For boolean expressions
        pass

    # For addition or subtraction
    def add_subract(self):
        return self.binary_op(self.modulo_multiply_divide, ("ADD_OP", "SUB_OP"))

    # For multiplication or division
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
            expr = self.expr()

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

    # BOOLEAN EXPRESSIONS
    # def comp_expr(self):
    #     res = ParseResult()

    #     if self.current_token.type == "NOT_OP":
    #         # Get "not" token
    #         not_token = self.current_token
    #         res.register_advancement()
    #         self.read_token()

    #         # Recursively get comparison expr
    #         node = res.register(self.comp_expr())

    #         if res.error:
    #             return res

    #         res.success(UnaryOpNode(not_token, node))

    #     # For binary boolean expressions
    #     node = res.register(self.binary_op(
    #         self.add_sub_expr,
    #         ("LT_OP", "GT_OP", "LTE_OP", "GTE_OP", "EQ_OP", "NEQ_OP"))
    #     )

    #     if res.error:
    #         return res.failure(InvalidSyntaxError(
    #             self.current_token.start_pos,
    #             self.current_token.end_pos,
    #             "Expected int, float, identifier, '+', '-', '(', or 'not'"
    #         ))

    #     return res.success(node)

    # def condition_stmt(self):
    #     res = ParseResult()

    #     # Read "if" token
    #     res.register_advancement()
    #     self.read_token()

    #     if_case = None
    #     elif_cases = []
    #     else_body = None

    #     # if condition
    #     self.cond_expr(res)

    #     # if body
    #     self.code_block(res)

    #     # elifs
    #     while self.current_token.matches("KEYWORD", "elif"):
    #         res.register_advancement()
    #         self.read_token()

    #         # elif condition
    #         self.cond_expr(res)

    #         # elif body
    #         self.code_block(res)

    #     # else
    #     if self.current_token.matches("KEYWORD", "else"):
    #         res.register_advancement()
    #         self.read_token()

    #         # else body
    #         self.code_block(res)

    #     return res.success(ConditionStmtNode(if_case, elif_cases, else_body))

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

    def code_block(self):
        # Check if next token is "{"
        if not self.current_token.type == "LBRACE_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '{'"
            )
        self.read_token()

        # Get block body
        body = self.stmt()

        # Check if next token is "}"
        if not self.current_token.type == "RBRACE_DELIM":
            return InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '}'"
            )
        self.read_token()

        return body

    # def cond_expr(self, res):
    #     # Check if next token is "("
    #     if not self.current_token.type == "LPAREN_DELIM":
    #         return res.failure(InvalidSyntaxError(
    #             self.current_token.start_pos,
    #             self.current_token.end_pos,
    #             "Expected '('"
    #         ))
    #     res.register_advancement()
    #     self.read_token()

    #     # TODO Get condition expr - change this to bool_expr later
    #     res.register(self.stmt())
    #     if res.error:
    #         return res

    #     # Check if next token is ")"
    #     if not self.current_token.type == "RPAREN_DELIM":
    #         return res.failure(InvalidSyntaxError(
    #             self.current_token.start_pos,
    #             self.current_token.end_pos,
    #             "Expected ')'"
    #         ))
    #     res.register_advancement()
    #     self.read_token()
