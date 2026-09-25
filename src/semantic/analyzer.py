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


class SemanticError(Exception):
    pass


class SemanticAnalyzer:

    def __init__(self):
        self.symbols = {}

    # -------------------------
    # Analyze Program
    # -------------------------

    def analyze(self, program):

        if not isinstance(program, Program):
            raise SemanticError("Invalid program")

        for statement in program.statements:
            self.visit(statement)

        return True

    # -------------------------
    # Visit Statement
    # -------------------------

    def visit(self, node):

        if isinstance(node, VarDeclaration):
            return self.visit_variable_declaration(node)

        if isinstance(node, Assignment):
            return self.visit_assignment(node)

        if isinstance(node, IfStatement):
            return self.visit_if(node)

        if isinstance(node, DoWhileStatement):
            return self.visit_do_while(node)

        if isinstance(node, PrintStatement):
            return self.visit_print(node)

        if isinstance(node, Block):
            return self.visit_block(node)

        if isinstance(node, BinaryExpression):
            return self.visit_binary(node)

        if isinstance(node, UnaryExpression):
            return self.visit_unary(node)

        if isinstance(node, Identifier):
            return self.visit_identifier(node)

        if isinstance(
            node,
            (
                NumberLiteral,
                DecimalLiteral,
                StringLiteral,
                BooleanLiteral,
            ),
        ):
            return self.visit_literal(node)

        raise SemanticError(
            f"Unknown AST node: {type(node).__name__}"
        )

    # -------------------------
    # Variable Declaration
    # -------------------------

    def visit_variable_declaration(self, node):

        if node.name in self.symbols:
            raise SemanticError(
                f"Variable '{node.name}' already declared"
            )

        value_type = self.visit(node.expression)

        if not self.is_valid_type(node.data_type, value_type):
            raise SemanticError(
                f"Type mismatch: variable '{node.name}' "
                f"is {node.data_type} but got {value_type}"
            )

        self.symbols[node.name] = node.data_type

    # -------------------------
    # Assignmentpython
    # -------------------------

    def visit_assignment(self, node):

        if node.name not in self.symbols:
            raise SemanticError(
                f"Variable '{node.name}' not declared"
            )

        value_type = self.visit(node.expression)

        variable_type = self.symbols[node.name]

        if not self.is_valid_type(variable_type, value_type):
            raise SemanticError(
                f"Type mismatch: variable '{node.name}' "
                f"is {variable_type} but got {value_type}"
            )

    # -------------------------
    # If Statement
    # -------------------------

    def visit_if(self, node):

        condition_type = self.visit(node.condition)

        if condition_type != "logic":
            raise SemanticError(
                "If condition must be logic"
            )

        self.visit(node.then_block)

        if node.else_block is not None:
            self.visit(node.else_block)

    # -------------------------
    # Do While
    # -------------------------

    def visit_do_while(self, node):

        self.visit(node.body)

        condition_type = self.visit(node.condition)

        if condition_type != "logic":
            raise SemanticError(
                "Do-while condition must be logic"
            )

    # -------------------------
    # Block
    # -------------------------

    def visit_block(self, node):

        for statement in node.statements:
            self.visit(statement)

    # -------------------------
    # Print
    # -------------------------

    def visit_print(self, node):

        self.visit(node.expression)

    # -------------------------
    # Identifier
    # -------------------------

    def visit_identifier(self, node):

        if node.name not in self.symbols:
            raise SemanticError(
                f"Variable '{node.name}' not declared"
            )

        return self.symbols[node.name]

    # -------------------------
    # Literals
    # -------------------------

    def visit_literal(self, node):

        if isinstance(node, NumberLiteral):
            return "num"

        if isinstance(node, DecimalLiteral):
            return "decimal"

        if isinstance(node, StringLiteral):
            return "text"

        if isinstance(node, BooleanLiteral):
            return "logic"

    # -------------------------
    # Unary Expression
    # -------------------------

    def visit_unary(self, node):

        operand_type = self.visit(node.operand)

        if node.operator == "!":

            if operand_type != "logic":
                raise SemanticError(
                    "NOT operator requires logic value"
                )

            return "logic"

        raise SemanticError(
            f"Unknown unary operator: {node.operator}"
        )

    # -------------------------
    # Binary Expression
    # -------------------------

    def visit_binary(self, node):

        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        operator = node.operator

        # Arithmetic
        if operator in {"+", "-", "*", "/", "%"}:

            if operator == "+" and (
                left_type == "text"
                or right_type == "text"
            ):
                if left_type == "text" and right_type == "text":
                    return "text"

            if left_type == "num" and right_type == "num":
                return "num"

            if (
                left_type in {"num", "decimal"}
                and right_type in {"num", "decimal"}
            ):
                return "decimal"

            raise SemanticError(
                f"Invalid arithmetic operation: "
                f"{left_type} {operator} {right_type}"
            )

        # Comparison
        if operator in {
            "<",
            ">",
            "<=",
            ">=",
        }:

            if left_type in {"num", "decimal"} and \
               right_type in {"num", "decimal"}:

                return "logic"

            raise SemanticError(
                "Comparison requires numeric values"
            )

        # Equality
        if operator in {"==", "!="}:

            if left_type == right_type:
                return "logic"

            raise SemanticError(
                "Equality comparison requires same types"
            )

        # Logical
        if operator in {"&&", "||"}:

            if left_type == "logic" and right_type == "logic":
                return "logic"

            raise SemanticError(
                "Logical operators require logic values"
            )

        raise SemanticError(
            f"Unknown binary operator: {operator}"
        )

    # -------------------------
    # Type Checking
    # -------------------------

    def is_valid_type(self, expected, actual):

        if expected == actual:
            return True

        # Allow integer value for decimal variable
        if expected == "decimal" and actual == "num":
            return True

        return False