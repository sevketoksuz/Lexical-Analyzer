import unittest

from analyzer.lexer import Lexer
from analyzer.parser import parse


class TestParser(unittest.TestCase):

    def print_tokens(self, tokens):
        print("Tokens:")
        for token in tokens:
            print(token)
        print()

    def print_parse_tree(self, node, level=0):
        indent = "  " * level
        print(f"{indent}Node(type={node.type}, value={node.value})")
        for child in node.children:
            self.print_parse_tree(child, level + 1)

    def test_parse_complex_expression(self):
        code = "x = (5 + 3) * (2 + 4);"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_parse_multiple_statements(self):
        code = "x = 5; y = x + 3.14; if (y > 10) { z = y * 2; }"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_parse_variable_assignment(self):
        code = "x = 5 + 3.14;"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_parse_if_statement(self):
        code = "if (x > 10) { y = 2.0 * x; }"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_parse_nested_if_statements(self):
        code = "if (x > 10) { if (y < 20) { z = y * 2; } }"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_parse_logical_expression(self):
        code = "if (x > 10 && y < 20) { z = y * 2; }"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        self.print_tokens(tokens)
        parse_tree = parse(tokens)
        self.print_parse_tree(parse_tree)
        self.assertIsNotNone(parse_tree)

    def test_syntax_error_missing_semicolon(self):
        code = "x = 5 + 3.14"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        with self.assertRaises(SyntaxError):
            self.print_tokens(tokens)
            parse_tree = parse(tokens)
            self.print_parse_tree(parse_tree)

    def test_syntax_error_unmatched_parenthesis(self):
        code = "if (x > 10 { y = 2.0 * x; }"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        with self.assertRaises(SyntaxError):
            self.print_tokens(tokens)
            parse_tree = parse(tokens)
            self.print_parse_tree(parse_tree)

    def test_syntax_error_unmatched_brace(self):
        code = "if (x > 10) { y = 2.0 * x;"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        with self.assertRaises(SyntaxError):
            self.print_tokens(tokens)
            parse_tree = parse(tokens)
            self.print_parse_tree(parse_tree)

    def test_syntax_error_invalid_variable_name(self):
        code = "1x = 5;"
        with self.assertRaises(SyntaxError):
            lexer = Lexer(code)
            tokens = lexer.get_tokens()
            self.print_tokens(tokens)
            parse_tree = parse(tokens)
            self.print_parse_tree(parse_tree)

    def test_syntax_error_invalid_operator(self):
        code = "x = 5 ** 2;"
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        with self.assertRaises(SyntaxError):
            self.print_tokens(tokens)
            parse_tree = parse(tokens)
            self.print_parse_tree(parse_tree)

if __name__ == '__main__':
    unittest.main()
