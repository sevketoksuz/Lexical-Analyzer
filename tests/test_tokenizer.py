import unittest
from analyzer.tokenizer import tokenize

class TestTokenizer(unittest.TestCase):

    def test_tokenize_variable_definitions(self):
        code = "myvar var_1 x2"
        expected_tokens = [
            {'type': 'IDENTIFIER', 'value': 'myvar'},
            {'type': 'IDENTIFIER', 'value': 'var_1'},
            {'type': 'IDENTIFIER', 'value': 'x2'}
        ]
        tokens = tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_keywords(self):
        code = "if else while for int float"
        expected_tokens = [
            {'type': 'KEYWORD', 'value': 'if'},
            {'type': 'KEYWORD', 'value': 'else'},
            {'type': 'KEYWORD', 'value': 'while'},
            {'type': 'KEYWORD', 'value': 'for'},
            {'type': 'KEYWORD', 'value': 'int'},
            {'type': 'KEYWORD', 'value': 'float'}
        ]
        tokens = tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_operators(self):
        code = "+ - * / % < > <= >= == != && || !"
        expected_tokens = [
            {'type': 'OPERATOR', 'value': '+'},
            {'type': 'OPERATOR', 'value': '-'},
            {'type': 'OPERATOR', 'value': '*'},
            {'type': 'OPERATOR', 'value': '/'},
            {'type': 'OPERATOR', 'value': '%'},
            {'type': 'OPERATOR', 'value': '<'},
            {'type': 'OPERATOR', 'value': '>'},
            {'type': 'OPERATOR', 'value': '<='},
            {'type': 'OPERATOR', 'value': '>='},
            {'type': 'OPERATOR', 'value': '=='},
            {'type': 'OPERATOR', 'value': '!='},
            {'type': 'OPERATOR', 'value': '&&'},
            {'type': 'OPERATOR', 'value': '||'},
            {'type': 'OPERATOR', 'value': '!'}
        ]
        tokens = tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_constants(self):
        code = "42 3.14"
        expected_tokens = [
            {'type': 'INTEGER', 'value': '42'},
            {'type': 'FLOAT', 'value': '3.14'}
        ]
        tokens = tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_whitespace(self):
        code = "x = 5 + 3.14"
        expected_tokens = [
            {'type': 'IDENTIFIER', 'value': 'x'},
            {'type': 'OPERATOR', 'value': '='},
            {'type': 'INTEGER', 'value': '5'},
            {'type': 'OPERATOR', 'value': '+'},
            {'type': 'FLOAT', 'value': '3.14'}
        ]
        tokens = tokenize(code)
        self.assertEqual(tokens, expected_tokens)

    def test_invalid_token(self):
        code = "1x = 5;"
        with self.assertRaises(SyntaxError):
            tokenize(code)

if __name__ == '__main__':
    unittest.main()
