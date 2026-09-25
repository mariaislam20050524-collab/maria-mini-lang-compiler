import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src")
)

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from codegen.codegen import CodeGenerator


def test_codegen_valid_program():

    source = Path(
        "tests/valid/test01_lexer.sl"
    ).read_text()

    tokens = Lexer(source).tokenize()

    ast = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()

    assert analyzer.analyze(ast) is True

    generator = CodeGenerator()

    output = generator.generate(ast)

    assert output is not None
    assert len(output) > 0
    assert "text name" in output
    assert "num x" in output
    assert "print" in output