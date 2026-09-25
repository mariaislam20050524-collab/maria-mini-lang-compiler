import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from lexer.lexer import Lexer
from lexer.errors import LexerError

from parser.parser import Parser, ParserError

from semantic.analyzer import SemanticAnalyzer, SemanticError

from codegen.codegen import CodeGenerator

from tac.tac import TACGenerator

from optimizer.optimizer import Optimizer


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

        # -------------------------
        # Semantic Analysis
        # -------------------------

        analyzer = SemanticAnalyzer()

        analyzer.analyze(ast)

        print("=== SEMANTIC ANALYSIS SUCCESS ===")
        print("No semantic errors found.")

        # -------------------------
        # Code Generation
        # -------------------------

        generator = CodeGenerator()

        output = generator.generate(ast)

        print("=== GENERATED CODE ===")
        print(output)

        # -------------------------
        # TAC Generation
        # -------------------------

        tac_generator = TACGenerator()

        tac = tac_generator.generate(ast)

        print("=== THREE ADDRESS CODE ===")

        for instruction in tac:
            print(instruction)

        # -------------------------
        # TAC Optimization
        # -------------------------

        optimizer = Optimizer()

        optimized_tac = optimizer.optimize(tac)

        print("=== OPTIMIZED TAC ===")

        for instruction in optimized_tac:
            print(instruction)

    except FileNotFoundError:

        print(f"File not found: {filename}")

    except LexerError as error:

        print(f"Lexer error: {error}")

    except ParserError as error:

        print(f"Parser error: {error}")

    except SemanticError as error:

        print(f"Semantic error: {error}")

    except Exception as error:

        print(f"Error: {error}")


if __name__ == "__main__":
    main()