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

Run the main script:

python main.py

code = "x = 5 + 3.14; if (x > 10) { y = 2.0 * x; }"
lexer = Lexer(code)
tokens = lexer.get_tokens()
parse_tree = parse(tokens)
print(parse_tree)