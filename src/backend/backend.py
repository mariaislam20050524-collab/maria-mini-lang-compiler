class Backend:

    def __init__(self):
        self.output = []

    def generate(self, instructions):

        self.output = []

        # -------------------------
        # Find labels
        # -------------------------

        labels = {}
        executable = []

        for instruction in instructions:

            instruction = instruction.strip()

            if not instruction:
                continue

            if instruction.endswith(":"):
                label = instruction[:-1]
                labels[label] = len(executable)
            else:
                executable.append(instruction)

        # -------------------------
        # Generate executable code
        # -------------------------

        lines = []

        lines.append("pc = 0")
        lines.append(f"while pc < {len(executable)}:")

        for index, instruction in enumerate(executable):

            prefix = "if" if index == 0 else "elif"

            lines.append(
                f"    {prefix} pc == {index}:"
            )

            # -------------------------
            # Print
            # -------------------------

            if instruction.startswith("print "):

                value = instruction[6:].strip()

                lines.append(
                    f"        print({self.convert_expression(value)})"
                )

                lines.append("        pc += 1")

            # -------------------------
            # ifFalse condition goto
            # -------------------------

            elif instruction.startswith("ifFalse "):

                parts = instruction.split()

                condition = parts[1]
                label = parts[3]

                target = labels[label]

                lines.append(
                    f"        if not {condition}:"
                )

                lines.append(
                    f"            pc = {target}"
                )

                lines.append("        else:")
                lines.append("            pc += 1")

            # -------------------------
            # if condition goto
            # -------------------------

            elif instruction.startswith("if "):

                parts = instruction.split()

                condition = parts[1]
                label = parts[3]

                target = labels[label]

                lines.append(
                    f"        if {condition}:"
                )

                lines.append(
                    f"            pc = {target}"
                )

                lines.append("        else:")
                lines.append("            pc += 1")

            # -------------------------
            # goto
            # -------------------------

            elif instruction.startswith("goto "):

                label = instruction.split()[1]

                target = labels[label]

                lines.append(
                    f"        pc = {target}"
                )

            # -------------------------
            # Assignment
            # -------------------------

            elif "=" in instruction:

                variable, expression = instruction.split(
                    "=",
                    1
                )

                variable = variable.strip()
                expression = expression.strip()

                expression = self.convert_expression(
                    expression
                )

                lines.append(
                    f"        {variable} = {expression}"
                )

                lines.append("        pc += 1")

            else:

                lines.append("        pc += 1")

        self.output = lines

        return "\n".join(lines)

    # -------------------------
    # Convert expressions
    # -------------------------

    def convert_expression(self, expression):

        expression = expression.replace(
            " true",
            " True"
        )

        expression = expression.replace(
            " false",
            " False"
        )

        expression = expression.replace(
            "true",
            "True"
        )

        expression = expression.replace(
            "false",
            "False"
        )

        expression = expression.replace(
            "&&",
            "and"
        )

        expression = expression.replace(
            "||",
            "or"
        )

        # TAC unary NOT: ! x
        expression = expression.replace(
            "! ",
            "not "
        )

        return expression

    # -------------------------
    # Execute generated code
    # -------------------------

    def execute(self, code):

        namespace = {}

        exec(code, {}, namespace)

        return namespace