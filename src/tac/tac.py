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


class TACGenerator:

    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.instructions.append(instruction)

    def generate(self, program):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

        self.visit(program)

        return self.instructions

    def visit(self, node):

        if isinstance(node, Program):
            for statement in node.statements:
                self.visit(statement)

        elif isinstance(node, Block):
            for statement in node.statements:
                self.visit(statement)

        elif isinstance(node, VarDeclaration):
            value = self.expression(node.expression)
            self.emit(f"{node.name} = {value}")

        elif isinstance(node, Assignment):
            value = self.expression(node.expression)
            self.emit(f"{node.name} = {value}")

        elif isinstance(node, PrintStatement):
            value = self.expression(node.expression)
            self.emit(f"print {value}")

        elif isinstance(node, IfStatement):

            condition = self.expression(node.condition)

            else_label = self.new_label()
            end_label = self.new_label()

            self.emit(
                f"ifFalse {condition} goto {else_label}"
            )

            self.visit(node.then_block)

            if node.else_block is not None:
                self.emit(f"goto {end_label}")
                self.emit(f"{else_label}:")
                self.visit(node.else_block)
                self.emit(f"{end_label}:")
            else:
                self.emit(f"{else_label}:")

        elif isinstance(node, DoWhileStatement):

            start_label = self.new_label()

            self.emit(f"{start_label}:")

            self.visit(node.body)

            condition = self.expression(node.condition)

            self.emit(
                f"if {condition} goto {start_label}"
            )

    def expression(self, node):

        if isinstance(node, NumberLiteral):
            return str(node.value)

        if isinstance(node, DecimalLiteral):
            return str(node.value)

        if isinstance(node, StringLiteral):
            return f'"{node.value}"'

        if isinstance(node, BooleanLiteral):
            return "true" if node.value else "false"

        if isinstance(node, Identifier):
            return node.name

        if isinstance(node, UnaryExpression):

            operand = self.expression(node.operand)

            temp = self.new_temp()

            self.emit(
                f"{temp} = {node.operator} {operand}"
            )

            return temp

        if isinstance(node, BinaryExpression):

            # Short-circuit AND
            if node.operator == "&&":

                left = self.expression(node.left)

                false_label = self.new_label()
                end_label = self.new_label()

                result = self.new_temp()

                self.emit(
                    f"ifFalse {left} goto {false_label}"
                )

                right = self.expression(node.right)

                self.emit(
                    f"{result} = {right}"
                )

                self.emit(
                    f"goto {end_label}"
                )

                self.emit(
                    f"{false_label}:"
                )

                self.emit(
                    f"{result} = false"
                )

                self.emit(
                    f"{end_label}:"
                )

                return result

            # Short-circuit OR
            if node.operator == "||":

                left = self.expression(node.left)

                true_label = self.new_label()
                end_label = self.new_label()

                result = self.new_temp()

                self.emit(
                    f"if {left} goto {true_label}"
                )

                right = self.expression(node.right)

                self.emit(
                    f"{result} = {right}"
                )

                self.emit(
                    f"goto {end_label}"
                )

                self.emit(
                    f"{true_label}:"
                )

                self.emit(
                    f"{result} = true"
                )

                self.emit(
                    f"{end_label}:"
                )

                return result

            left = self.expression(node.left)
            right = self.expression(node.right)

            temp = self.new_temp()

            self.emit(
                f"{temp} = {left} {node.operator} {right}"
            )

            return temp

        raise ValueError(
            f"Unknown expression: {type(node).__name__}"
        )