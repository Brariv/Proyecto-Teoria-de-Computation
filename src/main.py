from parsing.ast import astToGraph, postfixToAst
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader


if __name__ == "__main__":
    filename = input("Enter the path to the text file: ")
    lines = fileReader(filename) 

    for line in lines:
        postfix = infixToPostfix(line)

        ast = postfixToAst(postfix)

        # for showing the Ast
        astToGraph(ast).render(f'sintax_tree_{lines.index(line) + 1}', format='png', cleanup=True)



