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
from optimizer.optimizer import Optimizer
from backend.backend import Backend


def test_backend_execution():

    source = Path(
        "tests/valid/test_optimization.sl"
    ).read_text()

    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()

    analyzer = SemanticAnalyzer()
    assert analyzer.analyze(ast) is True

    tac_generator = TACGenerator()
    tac = tac_generator.generate(ast)

    optimizer = Optimizer()
    optimized_tac = optimizer.optimize(tac)

    backend = Backend()
    executable_code = backend.generate(
        optimized_tac
    )

    assert executable_code is not None
    assert "print(b)" in executable_code

    namespace = backend.execute(
        executable_code
    )

    assert namespace["a"] == 5
    assert namespace["b"] == 9