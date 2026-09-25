from lexer.token import Token
from parser.ast import (
    Program,
    Block,
    VarDeclaration,
    Assignment,
    IfStatement,
    DoWhileStatement,
    PrintStatement,
    BinaryExpression,
    UnaryExpression,
    NumberLiteral,
    DecimalLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
)


class ParserError(Exception):
    pass


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    # -------------------------
    # Basic parser functions
    # -------------------------

    def current(self):
        return self.tokens[self.position]

    def peek(self, token_type):
        return self.current().type == token_type

    def advance(self):
        token = self.current()

        if self.position < len(self.tokens) - 1:
            self.position += 1

        return token

    def expect(self, token_type):
        if not self.peek(token_type):
            token = self.current()

            raise ParserError(
                f"Expected {token_type} at "
                f"line {token.line}, column {token.column}, "
                f"but found {token.type}"
            )

        return self.advance()

    # -------------------------
    # Program
    # -------------------------

    def parse(self):
        self.expect("START")

        statements = self.parse_block_statements()

        self.expect("EOF")

        return Program(statements)

    # -------------------------
    # Block
    # -------------------------

    def parse_block_statements(self):
        self.expect("LBRACE")

        statements = []

        while not self.peek("RBRACE") and not self.peek("EOF"):
            statements.append(self.parse_statement())

        self.expect("RBRACE")

        return statements

    # -------------------------
    # Statement
    # -------------------------

    def parse_statement(self):

        # Variable declaration
        if self.peek("TEXT"):
            return self.parse_variable_declaration("text")

        if self.peek("NUM"):
            return self.parse_variable_declaration("num")

        if self.peek("DECIMAL"):
            return self.parse_variable_declaration("decimal")

        if self.peek("LOGIC"):
            return self.parse_variable_declaration("logic")

        # If statement
        if self.peek("IF"):
            return self.parse_if()

        # Do-while
        if self.peek("DO"):
            return self.parse_do_while()

        # Print
        if self.peek("PRINT"):
            return self.parse_print()

        # Assignment
        if self.peek("IDENTIFIER"):
            return self.parse_assignment()

        token = self.current()

        raise ParserError(
            f"Unexpected token {token.type} at "
            f"line {token.line}, column {token.column}"
        )

    # -------------------------
    # Variable declaration
    # -------------------------

    def parse_variable_declaration(self, data_type):

        self.advance()

        name = self.expect("IDENTIFIER").value

        self.expect("ASSIGN")

        expression = self.parse_expression()

        self.expect("SEMICOLON")

        return VarDeclaration(
            data_type,
            name,
            expression
        )

    # -------------------------
    # Assignment
    # -------------------------

    def parse_assignment(self):

        name = self.expect("IDENTIFIER").value

        self.expect("ASSIGN")

        expression = self.parse_expression()

        self.expect("SEMICOLON")

        return Assignment(
            name,
            expression
        )

    # -------------------------
    # If statement
    # -------------------------

    def parse_if(self):

        self.expect("IF")

        self.expect("LPAREN")

        condition = self.parse_expression()

        self.expect("RPAREN")

        then_block = Block(
            self.parse_block_statements()
        )

        else_block = None

        if self.peek("ELSE"):
            self.advance()

            else_block = Block(
                self.parse_block_statements()
            )

        return IfStatement(
            condition,
            then_block,
            else_block
        )

    # -------------------------
    # Do-while
    # -------------------------

    def parse_do_while(self):

        self.expect("DO")

        body = Block(
            self.parse_block_statements()
        )

        self.expect("WHILE")

        self.expect("LPAREN")

        condition = self.parse_expression()

        self.expect("RPAREN")

        self.expect("SEMICOLON")

        return DoWhileStatement(
            body,
            condition
        )

    # -------------------------
    # Print
    # -------------------------

    def parse_print(self):

        self.expect("PRINT")

        expression = self.parse_expression()

        self.expect("SEMICOLON")

        return PrintStatement(expression)

    # -------------------------
    # Expression
    # -------------------------

    def parse_expression(self):
        return self.parse_or()

    # OR: ||
    def parse_or(self):

        expression = self.parse_and()

        while self.peek("OR"):

            operator = self.advance().value

            right = self.parse_and()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # AND: &&
    def parse_and(self):

        expression = self.parse_equality()

        while self.peek("AND"):

            operator = self.advance().value

            right = self.parse_equality()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # == !=
    def parse_equality(self):

        expression = self.parse_comparison()

        while (
            self.peek("EQUAL")
            or self.peek("NOT_EQUAL")
        ):

            operator = self.advance().value

            right = self.parse_comparison()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # < > <= >=
    def parse_comparison(self):

        expression = self.parse_term()

        while (
            self.peek("LESS")
            or self.peek("GREATER")
            or self.peek("LESS_EQUAL")
            or self.peek("GREATER_EQUAL")
        ):

            operator = self.advance().value

            right = self.parse_term()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # + -
    def parse_term(self):

        expression = self.parse_factor()

        while (
            self.peek("PLUS")
            or self.peek("MINUS")
        ):

            operator = self.advance().value

            right = self.parse_factor()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # * / %
    def parse_factor(self):

        expression = self.parse_unary()

        while (
            self.peek("MULTIPLY")
            or self.peek("DIVIDE")
            or self.peek("MOD")
        ):

            operator = self.advance().value

            right = self.parse_unary()

            expression = BinaryExpression(
                expression,
                operator,
                right
            )

        return expression

    # ! unary
    def parse_unary(self):

        if self.peek("NOT"):

            operator = self.advance().value

            operand = self.parse_unary()

            return UnaryExpression(
                operator,
                operand
            )

        return self.parse_primary()

    # -------------------------
    # Primary expressions
    # -------------------------

    def parse_primary(self):

        token = self.current()

        if self.peek("NUMBER"):

            self.advance()

            return NumberLiteral(token.value)

        if self.peek("DECIMAL_LITERAL"):

            self.advance()

            return DecimalLiteral(token.value)

        if self.peek("STRING"):

            self.advance()

            return StringLiteral(token.value)

        if self.peek("TRUE"):

            self.advance()

            return BooleanLiteral(True)

        if self.peek("FALSE"):

            self.advance()

            return BooleanLiteral(False)

        if self.peek("IDENTIFIER"):

            self.advance()

            return Identifier(token.value)

        if self.peek("LPAREN"):

            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return expression

        raise ParserError(
            f"Unexpected token {token.type} at "
            f"line {token.line}, column {token.column}"
        )