class Node:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, children={self.children})"


def parse_primary(tokens, index):
    if index >= len(tokens):
        raise SyntaxError("Unexpected end of input")

    token = tokens[index]
    if token['type'] == 'SEPARATOR' and token['value'] == '(':
        expr_node, index = parse_expression(tokens, index + 1)
        if index >= len(tokens) or tokens[index]['type'] != 'SEPARATOR' or tokens[index]['value'] != ')':
            raise SyntaxError(f"Expected ')', but found {tokens[index] if index < len(tokens) else 'end of input'}")
        return expr_node, index + 1
    elif token['type'] in ('INTEGER', 'FLOAT', 'IDENTIFIER'):
        return Node(token['type'], token['value']), index + 1
    raise SyntaxError(f"Unexpected token: {token}")


def parse_term(tokens, index):
    node, index = parse_primary(tokens, index)
    while index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] in ('*', '/'):
        op_node = Node(tokens[index]['type'], tokens[index]['value'])
        index += 1
        right_node, index = parse_primary(tokens, index)
        op_node.add_child(node)
        op_node.add_child(right_node)
        node = op_node
    return node, index


def parse_expression(tokens, index):
    node, index = parse_term(tokens, index)
    while index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] in ('+', '-', '>', '<', '>=', '<=', '==', '!='):
        op_node = Node(tokens[index]['type'], tokens[index]['value'])
        index += 1
        right_node, index = parse_term(tokens, index)
        op_node.add_child(node)
        op_node.add_child(right_node)
        node = op_node
    return node, index


def parse_logical_expression(tokens, index):
    node, index = parse_expression(tokens, index)
    while index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] in ('&&', '||'):
        op_node = Node(tokens[index]['type'], tokens[index]['value'])
        index += 1
        right_node, index = parse_expression(tokens, index)
        op_node.add_child(node)
        op_node.add_child(right_node)
        node = op_node
    return node, index


def parse_assignment(tokens, index):
    if tokens[index]['type'] == 'IDENTIFIER':
        identifier_node = Node('IDENTIFIER', tokens[index]['value'])
        index += 1
        if index < len(tokens) and tokens[index]['type'] == 'OPERATOR' and tokens[index]['value'] == '=':
            operator_node = Node('OPERATOR', '=')
            operator_node.add_child(identifier_node)
            index += 1
            expr_node, index = parse_expression(tokens, index)
            operator_node.add_child(expr_node)
            if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == ';':
                semicolon_node = Node('SEPARATOR', tokens[index]['value'])
                semicolon_node.add_child(operator_node)
                return semicolon_node, index + 1
            raise SyntaxError(f"Expected ';' after assignment, but found {tokens[index] if index < len(tokens) else 'end of input'}")
        raise SyntaxError(f"Expected '=' after identifier, but found {tokens[index] if index < len(tokens) else 'end of input'}")
    raise SyntaxError(f"Expected identifier at the beginning of assignment, but found {tokens[index] if index < len(tokens) else 'end of input'}")


def parse_statement(tokens, index):
    if tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'if':
        return parse_if_statement(tokens, index)
    elif tokens[index]['type'] == 'IDENTIFIER':
        return parse_assignment(tokens, index)
    else:
        expr_node, index = parse_expression(tokens, index)
        if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == ';':
            semicolon_node = Node('SEPARATOR', tokens[index]['value'])
            semicolon_node.add_child(expr_node)
            return semicolon_node, index + 1
        raise SyntaxError(f"Expected ';' after expression, but found {tokens[index]}")


def parse_if_statement(tokens, index):
    if tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'if':
        if_node = Node('KEYWORD', 'if')
        index += 1
        if tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '(':
            index += 1
            condition_node, index = parse_logical_expression(tokens, index)
            if tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == ')':
                index += 1
                if_node.add_child(condition_node)
                block_node, index = parse_block(tokens, index)
                if_node.add_child(block_node)
                if index < len(tokens) and tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'else':
                    else_node = Node('KEYWORD', 'else')
                    index += 1
                    if index < len(tokens) and tokens[index]['type'] == 'KEYWORD' and tokens[index]['value'] == 'if':
                        else_if_node, index = parse_if_statement(tokens, index)
                        else_node.add_child(else_if_node)
                    else:
                        else_block_node, index = parse_block(tokens, index)
                        else_node.add_child(else_block_node)
                    if_node.add_child(else_node)
                return if_node, index
            else:
                raise SyntaxError(f"Expected ')' after condition, but found {tokens[index]}")
        else:
            raise SyntaxError(f"Expected '(' after 'if', but found {tokens[index]}")
    else:
        raise SyntaxError(f"Expected 'if' keyword, but found {tokens[index]}")


def parse_block(tokens, index):
    if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '{':
        block_node = Node('BLOCK', '{')
        index += 1
        while index < len(tokens) and not (tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '}'):
            statement_node, index = parse_statement(tokens, index)
            block_node.add_child(statement_node)
        if index < len(tokens) and tokens[index]['type'] == 'SEPARATOR' and tokens[index]['value'] == '}':
            return block_node, index + 1
        else:
            raise SyntaxError(f"Unmatched '{{', but found {tokens[index] if index < len(tokens) else 'end of input'}")
    raise SyntaxError(f"Expected '{{' to start block, but found {tokens[index]}")


def parse_program(tokens):
    program_node = Node('PROGRAM', 'program')
    index = 0
    while index < len(tokens):
        statement_node, index = parse_statement(tokens, index)
        program_node.add_child(statement_node)
    return program_node


def parse(tokens):
    parse_tree = parse_program(tokens)
    return parse_tree