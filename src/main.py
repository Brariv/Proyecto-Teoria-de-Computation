from parsing.ast import astToGraph, postfixToAst
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader


if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    for line in lines:
        postfix = infixToPostfix(line)

        ast = postfixToAst(postfix)

        astToGraph(ast).render(f'sintax_tree_{lines.index(line) + 1}', format='png', cleanup=True)
        # for showing the Ast



