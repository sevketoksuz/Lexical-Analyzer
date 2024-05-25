from analyzer.lexer import Lexer
from analyzer.parser import parse
from graphviz import Digraph
import os

# This should be the Graphviz library's location on PATH
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

def visualize_parse_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()

    graph.node(str(id(node)), f"{node.type}: {node.value}")

    if parent is not None:
        graph.edge(str(id(parent)), str(id(node)))

    for child in node.children:
        visualize_parse_tree(child, graph, node)

    return graph

def main():
    code = "x = 5 + 3.14; if (x > 10) { y = 2.0 * x; }"
    lexer = Lexer(code)
    tokens = lexer.get_tokens()
    for token in tokens:
        print(token)

    parse_tree = parse(tokens)
    graph = visualize_parse_tree(parse_tree)
    graph.render('parse_tree', format='png', view=True)

if __name__ == "__main__":
    main()
