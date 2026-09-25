import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from lexer.lexer import Lexer
from lexer.errors import LexerError
from parser.parser import Parser, ParserError


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <source-file>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source_code = file.read()

        # -------------------------
        # Lexer
        # -------------------------

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print("=== LEXER SUCCESS ===")
        print(f"Total tokens: {len(tokens)}")

        # -------------------------
        # Parser
        # -------------------------

        parser = Parser(tokens)
        ast = parser.parse()

        print("=== PARSER SUCCESS ===")
        print("Program parsed successfully.")

        print("=== AST ===")
        print(ast)

    except FileNotFoundError:
        print(f"File not found: {filename}")

    except LexerError as error:
        print(error)

    except ParserError as error:
        print(f"Parser error: {error}")


if __name__ == "__main__":
    main()
