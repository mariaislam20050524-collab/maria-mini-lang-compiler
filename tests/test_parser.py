import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lexer.lexer import Lexer
from parser.parser import Parser


def test_parser_valid_program():
    source = Path(
        "tests/valid/test01_lexer.sl"
    ).read_text()

    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    assert ast is not None
    assert len(ast.statements) == 5