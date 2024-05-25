import re

TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(?:if|else|while|for|int|float)\b'),
    ('IDENTIFIER', r'\b[a-z][a-zA-Z0-9_]*\b'),
    ('FLOAT', r'\b\d+\.\d+\b'),
    ('INTEGER', r'\b\d+\b'),
    ('OPERATOR', r'==|!=|<=|>=|&&|\|\||[+\-*/%<>=!&|]'),
    ('SEPARATOR', r'[;{}()\[\],]'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN', r'.')
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def tokenize(code):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE':
            continue
        elif kind == 'UNKNOWN':
            raise SyntaxError(f'Unexpected character: {value}')
        tokens.append({'type': kind, 'value': value})
    return tokens
