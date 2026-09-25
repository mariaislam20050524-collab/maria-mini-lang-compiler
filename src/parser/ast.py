class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements!r})"


class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements!r})"


class VarDeclaration:
    def __init__(self, data_type, name, expression):
        self.data_type = data_type
        self.name = name
        self.expression = expression

    def __repr__(self):
        return (
            f"VarDeclaration("
            f"type={self.data_type!r}, "
            f"name={self.name!r}, "
            f"expression={self.expression!r})"
        )


class Assignment:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        return (
            f"Assignment("
            f"name={self.name!r}, "
            f"expression={self.expression!r})"
        )


class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return (
            f"IfStatement("
            f"condition={self.condition!r}, "
            f"then={self.then_block!r}, "
            f"else={self.else_block!r})"
        )


class DoWhileStatement:
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

    def __repr__(self):
        return (
            f"DoWhileStatement("
            f"body={self.body!r}, "
            f"condition={self.condition!r})"
        )


class PrintStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintStatement({self.expression!r})"


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"left={self.left!r}, "
            f"operator={self.operator!r}, "
            f"right={self.right!r})"
        )


class UnaryExpression:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return (
            f"UnaryExpression("
            f"operator={self.operator!r}, "
            f"operand={self.operand!r})"
        )


class NumberLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral({self.value!r})"


class DecimalLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"DecimalLiteral({self.value!r})"


class StringLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value!r})"


class BooleanLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value!r})"


class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name!r})"