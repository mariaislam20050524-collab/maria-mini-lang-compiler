import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "src")
)

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analyzer import SemanticAnalyzer
from tac.tac import TACGenerator


def test_tac_generation():

    source = Path(
        "tests/valid/test01_lexer.sl"
    ).read_text()

    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    assert analyzer.analyze(ast) is True

    generator = TACGenerator()
    tac = generator.generate(ast)

    assert tac is not None
    assert len(tac) > 0

    # Check important TAC instructions
    assert any("name =" in instruction for instruction in tac)
    assert any("x =" in instruction for instruction in tac)
    assert any("print" in instruction for instruction in tac)
    assert any("goto" in instruction for instruction in tac)