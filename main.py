from analyzer.lexer import Lexer
from analyzer.parser import parse
from graphviz import Digraph
import os

# This should be the Graphviz library's location on PATH, 
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
    code = """
    a = 10 * (2 + 3);
    if (a < 50) {
        b = a - 10;
        if (b > 20) {
            c = b / 2;
            if (c == 10) {
                d = c * 3.14;
            } else {
                e = d + 5;
            }
        } else if (b == 10 || b == 15) {
            f = b + 5;
            if (f > 20 && f < 30) {
                g = f * 2;
            }
        } else {
            h = b - 1;
        }
    } else {
        i = a + 5;
    }
    x = (a + b) * (c - d);
    y = x / 2 + (f - g) * h;
    if (x > y) {
        result = x;
    } else {
        result = y;
    }
    """
    lexer = Lexer(code)
    tokens = lexer.get_tokens()
    for token in tokens:
        print(token)

    parse_tree = parse(tokens)
    graph = visualize_parse_tree(parse_tree)
    graph.render('parse_tree', format='png', view=True)

if __name__ == "__main__":
    main()
