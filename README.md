# Lexical Analyzer and Parser

This project provides a simple lexical analyzer (lexer) and parser for a custom language. It includes the following components:

- **Lexer**: Tokenizes input code into a series of tokens.
- **Parser**: Parses the tokens into an abstract syntax tree (AST).
- **AST Visualizer**: Visualizes the AST using Graphviz.

## Features

- Supports basic arithmetic operations.
- Handles variable assignments.
- Supports conditional statements (`if` statements).
- Visualizes the parse tree using Graphviz.

## Usage

## Run the main script:

python main.py

- code = "x = 5 + 3.14; if (x > 10) { y = 2.0 * x; }"
- lexer = Lexer(code)
- tokens = lexer.get_tokens()
- parse_tree = parse(tokens)
- print(parse_tree)

## Run the tests:
- python -m unittest


## Additional tests

- "a = 10 * (2 + 3); if (a < 50) { b = a - 10; }",
- "if ((x + y) > 15) { z = x * y; }",
- "m = 4 / 2; n = m + 6; if (n != 10) { p = n - 1; }",
- "if (a == 5) { if (b > 10) { c = a + b; } }",
- "if (x > 10 || y < 20) { z = x + y; } else { z = x - y; }",
- "if ((x > 5 && y < 15) || z == 20) { result = x * y; }",
- "value = 3.14 * (radius * radius); if (value > 50) { area = value; }",
- "if (count >= 10) { if (sum <= 50) { average = sum / count; } }",
- "if (x > 10 && y < 20) { z = x * 2; } else { z = y * 2; }",
- "if (a > b) { max = a; } else { max = b; }"