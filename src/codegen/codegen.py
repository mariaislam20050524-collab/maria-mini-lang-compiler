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


class CodeGenerator:

    def __init__(self):
        self.output = []
        self.indent = 0

    def generate(self, program):

        self.output = []
        self.indent = 0

        self.visit(program)

        return "\n".join(self.output)

    def emit(self, line):

        spaces = "    " * self.indent

        self.output.append(
            spaces + line
        )

    def visit(self, node):

        if isinstance(node, Program):

            for statement in node.statements:
                self.visit(statement)

        elif isinstance(node, Block):

            self.emit("{")

            self.indent += 1

            for statement in node.statements:
                self.visit(statement)

            self.indent -= 1

            self.emit("}")

        elif isinstance(node, VarDeclaration):

            value = self.expression(node.expression)

            self.emit(
                f"{node.data_type} {node.name} = {value};"
            )

        elif isinstance(node, Assignment):

            value = self.expression(node.expression)

            self.emit(
                f"{node.name} = {value};"
            )

        elif isinstance(node, PrintStatement):

            value = self.expression(node.expression)

            self.emit(
                f"print({value});"
            )

        elif isinstance(node, IfStatement):

            condition = self.expression(
                node.condition
            )

            self.emit(
                f"if ({condition})"
            )

            self.visit(node.then_block)

            if node.else_block is not None:

                self.emit("else")

                self.visit(
                    node.else_block
                )

        elif isinstance(node, DoWhileStatement):

            self.emit("do")

            self.visit(node.body)

            condition = self.expression(
                node.condition
            )

            self.emit(
                f"while ({condition});"
            )

    def expression(self, node):

        if isinstance(node, NumberLiteral):

            return str(node.value)

        if isinstance(node, DecimalLiteral):

            return str(node.value)

        if isinstance(node, StringLiteral):

            value = node.value.replace(
                "\\",
                "\\\\"
            ).replace(
                '"',
                '\\"'
            )

            return f'"{value}"'

        if isinstance(node, BooleanLiteral):

            return (
                "true"
                if node.value
                else "false"
            )

        if isinstance(node, Identifier):

            return node.name

        if isinstance(node, UnaryExpression):

            operand = self.expression(
                node.operand
            )

            return (
                f"({node.operator}{operand})"
            )

        if isinstance(node, BinaryExpression):

            left = self.expression(
                node.left
            )

            if node.operator == "&&":

                right = self.expression(
                    node.right
                )

                return (
                    f"({left} and {right})"
                )

            if node.operator == "||":

                right = self.expression(
                    node.right
                )

                return (
                    f"({left} or {right})"
                )

            right = self.expression(
                node.right
            )

            return (
                f"({left} "
                f"{node.operator} "
                f"{right})"
            )

        raise ValueError(
            f"Unknown expression: "
            f"{type(node).__name__}"
        )