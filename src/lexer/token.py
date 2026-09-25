from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token("
            f"type={self.type!r}, "
            f"value={self.value!r}, "
            f"line={self.line}, "
            f"column={self.column}"
            f")"
        )
