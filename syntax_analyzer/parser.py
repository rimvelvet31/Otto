from syntax_analyzer.nodes import *
from syntax_analyzer.parse_result import ParseResult
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

    # Entry point for parser
    def otto_progstmt(self):
        # TODO change stmt to body later for multiple lines
        res = self.stmt()

        # Check if parsing was terminated while there are still tokens to parse
        if not res.error and self.current_token.type != "EOF":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected arithmetic or boolean operator"
            ))

        return res

    # LITERALS
    def atom(self):
        res = ParseResult()
        token = self.current_token

        # For numbers
        if token.type in ("INT", "FLOAT"):
            res.register_advancement()
            self.read_token()
            return res.success(NumberNode(token))

        # For strings
        elif token.type == "STRING":
            res.register_advancement()
            self.read_token()
            return res.success(StringNode(token))

        # For identifiers
        elif token.type == "IDENTIFIER":
            res.register_advancement()
            self.read_token()
            return res.success(IdentifierNode(token))

        # For parenthesis expressions
        elif token.type == "LPAREN_DELIM":
            res.register_advancement()
            self.read_token()

            expr = res.register(self.stmt())
            if res.error:
                return res

            # Check if parenthesis is closed
            if self.current_token.type == "RPAREN_DELIM":
                res.register_advancement()
                self.read_token()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.start_pos,
                    self.current_token.end_pos,
                    "Expected ')'"
                ))

        # DISREGARD FOR NOW
        # For list expressions
        # elif token.type == "LBRACK_DELIM":
        #     list_expr = res.register(self.list_expr())
        #     if res.error:
        #         return res
        #     return res.success(list_expr)

        return res.failure(InvalidSyntaxError(
            token.start_pos,
            token.end_pos,
            "Expected a literal value (int, float, string, identifier)"
        ))

    # ARITHMETIC EXPRESSIONS
    def power(self):
        return self.binary_op(self.atom, ("POW_OP",), self.factor)

    # For unary operation or exponentiationq
    def factor(self):
        res = ParseResult()
        token = self.current_token

        # For unary operation (positive or negative nums)
        if token.type in ("ADD_OP", "SUB_OP"):
            res.register_advancement()
            self.read_token()
            factor = res.register(self.factor())

            if res.error:
                return res

            return res.success(UnaryOpNode(token, factor))

        # For exponentiation
        return self.power()

    # For multiplication or division
    def term(self):
        return self.binary_op(self.factor, ("MUL_OP", "DIV_OP"))

    # For addition or subtraction
    def add_sub_expr(self):
        return self.binary_op(self.term, ("ADD_OP", "SUB_OP"))

    # BOOLEAN EXPRESSIONS
    def comp_expr(self):
        res = ParseResult()

        if self.current_token.type == "NOT_OP":
            # Get "not" token
            not_token = self.current_token
            res.register_advancement()
            self.read_token()

            # Recursively get comparison expr
            node = res.register(self.comp_expr())

            if res.error:
                return res

            res.success(UnaryOpNode(not_token, node))

        # For binary boolean expressions
        node = res.register(self.binary_op(
            self.add_sub_expr,
            ("LT_OP", "GT_OP", "LTE_OP", "GTE_OP", "EQ_OP", "NEQ_OP"))
        )

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected int, float, identifier, '+', '-', '(', or 'not'"
            ))

        return res.success(node)

    def stmt(self):
        res = ParseResult()

        # For assignment or input statements
        if self.current_token.type == "IDENTIFIER":
            identifier = self.current_token
            res.register_advancement()
            self.read_token()

            # For assignment statement
            if self.current_token.type == "ASSIGN_OP":
                # Read "=" token
                res.register_advancement()
                self.read_token()

                # Go to input_stmt if "input" keyword is found
                if self.current_token.matches("KEYWORD", "input"):
                    return self.input_stmt(res, identifier)

                # Otherwise, go to assign_stmt
                return self.assign_stmt(res, identifier)

            # TODO add identifier in arith & bool expressions

        # For output statement
        if self.current_token.matches("KEYWORD", "utter"):
            output_stmt = res.register(self.output_stmt(res))
            if res.error:
                return res
            return res.success(output_stmt)

        # For condition statements
        if self.current_token.matches("KEYWORD", "if"):
            condition_stmt = res.register(self.condition_stmt())
            if res.error:
                return res
            return res.success(condition_stmt)

        # For iterative statements
        if self.current_token.matches("KEYWORD", "for"):
            pass

        if self.current_token.matches("KEYWORD", "while"):
            pass

        # TODO For arithmetic or boolean expressions
        node = res.register(
            self.binary_op(self.comp_expr, ("AND_OP", "OR_OP"))
        )

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected a statement or expression"
            ))

        # Check for semicolon
        if self.current_token.type == "SEMI_DELIM":
            # Read ";" token
            res.register_advancement()
            self.read_token()
        else:
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ';' at the end of the statement"
            ))

        return res.success(node)

    def binary_op(self, left_nonterminal, accepted_ops, right_nonterminal=None):
        # Both left and right nonterminals are the same
        if right_nonterminal is None:
            right_nonterminal = left_nonterminal

        res = ParseResult()
        left_node = res.register(left_nonterminal())

        if res.error:
            return res

        while self.current_token.type in accepted_ops:
            op_token = self.current_token
            res.register_advancement()
            self.read_token()

            # Recursively call non_terminal to get right node
            right_node = res.register(right_nonterminal())

            if res.error:
                return res

            left_node = BinaryOpNode(left_node, op_token, right_node)

        return res.success(left_node)

    # STATEMENTS
    def assign_stmt(self, res, identifier):
        value = res.register(self.stmt())
        if res.error:
            return res

        return res.success(AssignStmtNode(identifier, value))

    def input_stmt(self, res, identifier):
        # Read "input" keyword
        res.register_advancement()
        self.read_token()

        # Check if next token is "("
        if not self.current_token.type == "LPAREN_DELIM":
            return self.return_error("Expected '('")
        # Read "(" token
        res.register_advancement()
        self.read_token()

        # Parse input prompt
        prompt = res.register(self.atom())

        # Check if next token is ")"
        if not self.current_token.type == "RPAREN_DELIM":
            self.return_error("Expected ')'")
        # Read ")" token
        res.register_advancement()
        self.read_token()

        return res.success(InputStmtNode(identifier, prompt))

    def output_stmt(self, res):
        # Read "utter" keyword
        res.register_advancement()
        self.read_token()

        # Check if next token is "("
        if not self.current_token.type == "LPAREN_DELIM":
            return self.return_error("Expected '('")
        # Read "(" token
        res.register_advancement()
        self.read_token()

        # Parse output value
        value = res.register(self.atom())

        # Check if next token is ")"
        if not self.current_token.type == "RPAREN_DELIM":
            return self.return_error("Expected ')'")
        # Read ")" token
        res.register_advancement()
        self.read_token()

        # Check if next token is ";"
        if not self.current_token.type == "SEMI_DELIM":
            return self.return_error("Expected ';'")
        # Read ";" token
        res.register_advancement()
        self.read_token()

        return res.success(OutputStmtNode(value))

    def condition_stmt(self):
        res = ParseResult()

        # Read "if" token
        res.register_advancement()
        self.read_token()

        if_case = None
        elif_cases = []
        else_body = None

        # if condition
        self.cond_expr(res)

        # if body
        self.code_block(res)

        # elifs
        while self.current_token.matches("KEYWORD", "elif"):
            res.register_advancement()
            self.read_token()

            # elif condition
            self.cond_expr(res)

            # elif body
            self.code_block(res)

        # else
        if self.current_token.matches("KEYWORD", "else"):
            res.register_advancement()
            self.read_token()

            # else body
            self.code_block(res)

        return res.success(ConditionStmtNode(if_case, elif_cases, else_body))

    def for_stmt(self):
        pass

    def while_stmt(self):
        res = ParseResult()

        # Read "while" token
        res.register_advancement()
        self.read_token()

        # Parse condition
        condition = self.cond_expr(res)

        # Parse body
        body = self.code_block(res)

        return res.success(WhileStmtNode(condition, body))

    def uniq_stmt(self):
        pass

    # HELPER METHODS
    def code_block(self, res):
        # Check if next token is "{"
        if not self.current_token.type == "LBRACE_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '{'"
            ))
        res.register_advancement()
        self.read_token()

        # Get block body
        body = res.register(self.stmt())
        if res.error:
            return res

        # Check if next token is "}"
        if not self.current_token.type == "RBRACE_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '}'"
            ))
        res.register_advancement()
        self.read_token()

        return res.success(body)

    def cond_expr(self, res):
        # Check if next token is "("
        if not self.current_token.type == "LPAREN_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '('"
            ))
        res.register_advancement()
        self.read_token()

        # TODO Get condition expr - change this to bool_expr later
        res.register(self.stmt())
        if res.error:
            return res

        # Check if next token is ")"
        if not self.current_token.type == "RPAREN_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ')'"
            ))
        res.register_advancement()
        self.read_token()

    # DISREGARD FOR NOW
    def list_expr(self):
        res = ParseResult()
        elements = []

        # Check if next token is "["
        if not self.current_token.type == "LBRACK_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected '['"
            ))
        res.register_advancement()
        self.read_token()

        # If list is empty
        if self.current_token.type == "RBRACK_DELIM":
            res.register_advancement()
            self.read_token()
            return res.success(ListNode(elements))

        # If list is not empty
        elements.append(res.register(self.stmt()))
        if res.error:
            return res

        # Add more elements if there are any
        while self.current_token.type == "COMMA_DELIM":
            # Read ","
            res.register_advancement()
            self.read_token()

            elements.append(res.register(self.stmt()))
            if res.error:
                return res

        # Check if list is closed
        if self.current_token.type != "RBRACK_DELIM":
            return res.failure(InvalidSyntaxError(
                self.current_token.start_pos,
                self.current_token.end_pos,
                "Expected ',' or ']'"
            ))

        return res.success(ListNode(elements))

    # HELPER METHODS
    def return_error(self, message):
        return InvalidSyntaxError(
            self.current_token.start_pos,
            self.current_token.end_pos,
            message
        )
