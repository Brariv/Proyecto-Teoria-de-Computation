from match.nfa_match import matchStringToRegex
from parsing.ast import astToGraph, postfixToAst
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader


if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    print(lines)
    for line in lines:
        print(line)
        postfix = infixToPostfix(line)

        print(postfix)

        print(line,"a",matchStringToRegex(postfix,"bbb"))

        # for showing the Ast



