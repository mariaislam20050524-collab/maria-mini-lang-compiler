from .token import Token
from .errors import LexerError


# Custom keywords for our MiniLang variant
KEYWORDS = {
    "text": "TEXT",
    "num": "NUM",
    "decimal": "DECIMAL",
    "logic": "LOGIC",

    "yes": "TRUE",
    "no": "FALSE",

    "check": "IF",
    "otherwise": "ELSE",

    "do": "DO",
    "during": "WHILE",

    "func": "FUNCTION",
    "give": "RETURN",

    "show": "PRINT",

    "stop": "BREAK",
    "skip": "CONTINUE",

    "record": "RECORD",
    "start": "START",
}


class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    # Get current character
    def current_char(self):
        if self.position >= len(self.source):
            return "\0"

        return self.source[self.position]

    # Look at next character without moving
    def peek(self):
        if self.position + 1 >= len(self.source):
            return "\0"

        return self.source[self.position + 1]

    # Move to next character
    def advance(self):
        char = self.current_char()

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    # Skip spaces, tabs and new lines
    def skip_whitespace(self):
        while self.current_char() in " \t\r\n":
            self.advance()

    # Read identifier or keyword
    def read_identifier(self):
        start_line = self.line
        start_column = self.column

        value = ""

        while (
            self.current_char().isalnum()
            or self.current_char() == "_"
        ):
            value += self.advance()

        token_type = KEYWORDS.get(value, "IDENTIFIER")

        return Token(
            token_type,
            value,
            start_line,
            start_column
        )

    # Read integer or decimal number
    def read_number(self):
        start_line = self.line
        start_column = self.column

        value = ""

        while self.current_char().isdigit():
            value += self.advance()

        # Decimal number
        if (
            self.current_char() == "."
            and self.peek().isdigit()
        ):
            value += self.advance()

            while self.current_char().isdigit():
                value += self.advance()

            return Token(
                "DECIMAL_LITERAL",
                float(value),
                start_line,
                start_column
            )

        return Token(
            "NUMBER",
            int(value),
            start_line,
            start_column
        )

    # Read string
    def read_string(self):
        start_line = self.line
        start_column = self.column

        # Skip opening "
        self.advance()

        value = ""

        while self.current_char() not in ['"', "\0", "\n"]:

            # Handle escape characters
            if self.current_char() == "\\":
                self.advance()

                next_char = self.current_char()

                if next_char == "n":
                    value += "\n"
                elif next_char == "t":
                    value += "\t"
                elif next_char == '"':
                    value += '"'
                elif next_char == "\\":
                    value += "\\"
                else:
                    raise LexerError(
                        f"Invalid escape sequence: \\{next_char}",
                        self.line,
                        self.column
                    )

                self.advance()

            else:
                value += self.advance()

        # String was not closed
        if self.current_char() != '"':
            raise LexerError(
                "Unterminated string",
                start_line,
                start_column
            )

        # Skip closing "
        self.advance()

        return Token(
            "STRING",
            value,
            start_line,
            start_column
        )

    # Skip single-line comments
    def skip_comment(self):
        while (
            self.current_char() != "\n"
            and self.current_char() != "\0"
        ):
            self.advance()

    # Main tokenizing function
    def tokenize(self):

        tokens = []

        while self.current_char() != "\0":

            # Ignore whitespace
            if self.current_char() in " \t\r\n":
                self.skip_whitespace()
                continue

            # Comments
            if (
                self.current_char() == "/"
                and self.peek() == "/"
            ):
                self.skip_comment()
                continue

            line = self.line
            column = self.column
            char = self.current_char()

            # Identifier or keyword
            if char.isalpha() or char == "_":
                tokens.append(self.read_identifier())
                continue

            # Number
            if char.isdigit():
                tokens.append(self.read_number())
                continue

            # String
            if char == '"':
                tokens.append(self.read_string())
                continue

            # Two-character operators
            if char == "=" and self.peek() == "=":
                self.advance()
                self.advance()

                tokens.append(
                    Token("EQUAL", "==", line, column)
                )
                continue

            if char == "!" and self.peek() == "=":
                self.advance()
                self.advance()

                tokens.append(
                    Token("NOT_EQUAL", "!=", line, column)
                )
                continue

            if char == "<" and self.peek() == "=":
                self.advance()
                self.advance()

                tokens.append(
                    Token("LESS_EQUAL", "<=", line, column)
                )
                continue

            if char == ">" and self.peek() == "=":
                self.advance()
                self.advance()

                tokens.append(
                    Token("GREATER_EQUAL", ">=", line, column)
                )
                continue

            # Short-circuit AND
            if char == "&" and self.peek() == "&":
                self.advance()
                self.advance()

                tokens.append(
                    Token("AND", "&&", line, column)
                )
                continue

            # Short-circuit OR
            if char == "|" and self.peek() == "|":
                self.advance()
                self.advance()

                tokens.append(
                    Token("OR", "||", line, column)
                )
                continue

            # Single-character operators
            single_char_tokens = {
                "+": "PLUS",
                "-": "MINUS",
                "*": "MULTIPLY",
                "/": "DIVIDE",
                "%": "MOD",

                "=": "ASSIGN",

                "<": "LESS",
                ">": "GREATER",
                "!": "NOT",

                "(": "LPAREN",
                ")": "RPAREN",

                "{": "LBRACE",
                "}": "RBRACE",

                "[": "LBRACKET",
                "]": "RBRACKET",

                ";": "SEMICOLON",
                ",": "COMMA",
                ".": "DOT",
                ":": "COLON"
            }

            if char in single_char_tokens:

                token_type = single_char_tokens[char]

                self.advance()

                tokens.append(
                    Token(
                        token_type,
                        char,
                        line,
                        column
                    )
                )

                continue

            # Unknown character
            raise LexerError(
                f"Invalid character: {char!r}",
                line,
                column
            )

        # End of file token
        tokens.append(
            Token(
                "EOF",
                None,
                self.line,
                self.column
            )
        )

        return tokens
