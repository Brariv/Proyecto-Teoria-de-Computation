from match.nfa_match import matchStringToRegex
from parsing.ast import astToGraph, postfixToAst
from parsing.nfa import postfixToNfa
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader

import sys
sys.setrecursionlimit(10**8)

if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    string:str = "bbbbbbbbbbb"

    print(lines)
    for line in lines:
        postfix = infixToPostfix(line)

        afn = postfixToNfa(postfix)

        # for showing the Ast



