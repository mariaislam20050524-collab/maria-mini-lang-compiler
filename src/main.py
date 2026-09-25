import sys
from pathlib import Path

# Allow Python to find the lexer package
sys.path.append(str(Path(__file__).parent))

from lexer.lexer import Lexer
from lexer.errors import LexerError


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <source-file>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source_code = file.read()

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print("=== TOKENS ===")

        for token in tokens:
            print(token)

    except FileNotFoundError:
        print(f"File not found: {filename}")

    except LexerError as error:
        print(error)


if __name__ == "__main__":
    main()
