class Node:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, children={self.children})"


def parse_expression(tokens):
    def parse_primary(index):
        if index >= len(tokens):
            raise SyntaxError("Unexpected end of input")

        token = tokens[index]
        print(f"parse_primary: {token}")
        if token['type'] == 'SEPARATOR' and token['value'] == '(':
            expr_node, index = parse_expression(index + 1)
            if index >= len(tokens) or tokens[index]['type'] != 'SEPARATOR' or tokens[index]['value'] != ')':
                raise SyntaxError("Expected ')'")
            return expr_node, index + 1
        elif token['type'] in ('INTEGER', 'FLOAT', 'IDENTIFIER'):
            return Node(token['type'], token['value']), index + 1
        raise SyntaxError(f"Unexpected token: {token}")

    def parse_term(index):
        node, index = parse_primary(index)
        while index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] in ('*', '/'):
            op_node = Node(tokens[index]['type'], tokens[index]['value'])
            print(f"parse_term: operator {tokens[index]}")
            index += 1
            right_node, index = parse_primary(index)
            op_node.add_child(node)
            op_node.add_child(right_node)
            node = op_node
        return node, index

    def parse_expression(index):
        node, index = parse_term(index)
        while index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] in ('+', '-'):
            op_node = Node(tokens[index]['type'], tokens[index]['value'])
            print(f"parse_expression: operator {tokens[index]}")
            index += 1
            right_node, index = parse_term(index)
            op_node.add_child(node)
            op_node.add_child(right_node)
            node = op_node
        return node, index

    def parse_statement(index):
        if tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'if':
            return parse_if_statement(index)
        else:
            expr_node, index = parse_expression(index)
            if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == ';':
                semicolon_node = Node('SEPARATOR', tokens[index]['value'])
                semicolon_node.add_child(expr_node)
                return semicolon_node, index + 1
            raise SyntaxError("Expected ';' after expression")

    def parse_if_statement(index):
        if tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'if':
            if_node = Node('KEYWORD', 'if')
            index += 1
            if tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '(':
                index += 1
                condition_node, index = parse_expression(index)
                if tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == ')':
                    index += 1
                    if_node.add_child(condition_node)
                    block_node, index = parse_block(index)
                    if_node.add_child(block_node)
                    return if_node, index
                else:
                    raise SyntaxError(f"Expected ')' after condition, got {tokens[index]}")
            else:
                raise SyntaxError(f"Expected '(' after 'if', got {tokens[index]}")
        else:
            raise SyntaxError(f"Expected 'if' keyword, got {tokens[index]}")

    def parse_block(index):
        if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '{':
            block_node = Node('BLOCK', '{')
            index += 1
            while index < len(tokens) and not (tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '}'):
                statement_node, index = parse_statement(index)
                block_node.add_child(statement_node)
            if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '}':
                return block_node, index + 1
            else:
                raise SyntaxError(f"Unmatched '{{', got {tokens[index]}")
        raise SyntaxError(f"Expected '{{' to start block, got {tokens[index]}")

    def parse_program(index):
        program_node = Node('PROGRAM', 'program')
        while index < len(tokens):
            statement_node, index = parse_statement(index)
            program_node.add_child(statement_node)
        return program_node, index

    parse_tree, index = parse_program(0)
    if index != len(tokens):
        raise SyntaxError(f"Unexpected token at end: {tokens[index]}")
    return parse_tree
