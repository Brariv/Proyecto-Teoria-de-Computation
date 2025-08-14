from graphviz import *

def main():
    filename = input("Enter the path to the text file: ")
    lines = txtreader(filename) 

    for line in lines:
        print(f"Processing line: {line}")
        print("-" * 100)
        postfix = infixToPostfix(line)
        print("-" * 100)
        print(f"Postfix notation: {postfix}")
        print("=" * 100 + "\n")
        ast = AST(postfix)
        print(f"AST: {ast}")
        sintax_tree_graph = sintax_tree(ast)
        sintax_tree_graph.render(f'sintax_tree_{lines.index(line) + 1}', format='png', cleanup=True)
        print("=" * 100 + "\n")

main()
