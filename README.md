
# Maria Mini Language Compiler

A small compiler for the Maria Mini Language, developed as part of the Compiler Design Lab Assignment.

## Features

The compiler supports:

* Lexical analysis
* Recursive descent parsing
* Abstract Syntax Tree (AST)
* Semantic analysis
* Variable declarations
* Assignment statements
* Arithmetic expressions
* Comparison operators
* Logical operators
* Short-circuit `&&` and `||`
* Unary `!` operator
* String values and string concatenation
* `check` / `otherwise` conditional statements
* `do` / `during` loop
* Three Address Code (TAC) generation
* TAC optimization
* Backend code generation
* Program execution
* Error handling

## Project Structure

```text
maria-mini-lang-compiler/
│
├── src/
│   ├── lexer/
│   │   ├── lexer.py
│   │   └── errors.py
│   │
│   ├── parser/
│   │   ├── parser.py
│   │   └── ast.py
│   │
│   ├── semantic/
│   │   └── analyzer.py
│   │
│   ├── codegen/
│   │   └── codegen.py
│   │
│   ├── tac/
│   │   └── tac.py
│   │
│   ├── optimizer/
│   │   └── optimizer.py
│   │
│   ├── backend/
│   │   └── backend.py
│   │
│   └── main.py
│
├── tests/
│   ├── valid/
│   └── invalid/
│
├── README.md
└── REPORT.pdf
```

## Requirements

* Python 3
* pytest

Install pytest if necessary:

```bash
pip install pytest
```

## How to Run

Run a Maria Mini Language program using:

```bash
python src/main.py <source-file>
```

Example:

```bash
python src/main.py tests/valid/test01_lexer.sl
```

The compiler performs the following steps:

```text
Source Code
     ↓
Lexer
     ↓
Parser
     ↓
Semantic Analysis
     ↓
Code Generation
     ↓
Three Address Code
     ↓
Optimization
     ↓
Backend
     ↓
Program Execution
```

## Running Tests

Run all automated tests with:

```bash
pytest -q
```

The project also contains valid and invalid source programs for testing compiler behavior.

## Test Programs

The project contains more than 15 test programs.

### Valid Tests

The valid test programs cover:

* Strings
* String concatenation
* Arithmetic operations
* Logical operations
* Short-circuit evaluation
* Co
