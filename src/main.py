from drawing.nfa import nfaToDiGraph
from match.nfa_match import matchStringToNfa
from parsing.ast import astToGraph, postfixToAst
from parsing.nfa import postfixToNfa
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader

import sys
sys.setrecursionlimit(10**8)

if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    string:str = input("Add your cool string :D :")

    print(lines)
    for line in lines:
        postfix = infixToPostfix(line)

        nfa = postfixToNfa(postfix)

        # for showing the Ast

        if matchStringToNfa(nfa, string):
            print("yes")
        else:
            print("no")

        nfaToDiGraph(nfa).render(f"nfa_imgs/nfa_from_{line}", format="png", cleanup=True) # To lazy for having the count, just making a random tree



