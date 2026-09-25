class Optimizer:

    def __init__(self):
        self.constants = {}

    def optimize(self, instructions):

        self.constants = {}

        optimized = []

        for instruction in instructions:

            # --------------------------------
            # Constant Assignment
            # --------------------------------

            if "=" in instruction and not instruction.startswith(
                ("if", "goto")
            ):
                parts = instruction.split("=", 1)

                variable = parts[0].strip()
                value = parts[1].strip()

                # Constant propagation
                if value in self.constants:
                    value = self.constants[value]

                # Constant folding
                folded = self.constant_fold(value)

                if folded is not None:
                    value = folded
                    self.constants[variable] = value
                else:
                    self.constants.pop(variable, None)

                instruction = f"{variable} = {value}"

            optimized.append(instruction)

        return optimized

    def constant_fold(self, expression):

        parts = expression.split()

        if len(parts) != 3:
            return None

        left, operator, right = parts

        # Only fold numeric constants
        try:
            left_value = float(left)
            right_value = float(right)
        except ValueError:
            return None

        try:

            if operator == "+":
                result = left_value + right_value

            elif operator == "-":
                result = left_value - right_value

            elif operator == "*":
                result = left_value * right_value

            elif operator == "/":
                if right_value == 0:
                    return None
                result = left_value / right_value

            elif operator == "%":
                if right_value == 0:
                    return None
                result = left_value % right_value

            else:
                return None

            # Keep integer results clean
            if result.is_integer():
                return str(int(result))

            return str(result)

        except Exception:
            return None