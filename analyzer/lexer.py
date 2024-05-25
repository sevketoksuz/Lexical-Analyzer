from .tokenizer import tokenize

class Lexer:
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.position = 0

    def get_tokens(self):
        return self.tokens

    def next_token(self):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            self.position += 1
            return token
        return None

    def peek_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
