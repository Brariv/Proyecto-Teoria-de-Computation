from match.nfa_match import matchStringToRegex
from parsing.ast import astToGraph, postfixToAst
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader


if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    string:str = "a"

    print(lines)
    for line in lines:
        postfix = infixToPostfix(line)

        print(line,string,matchStringToRegex(postfix,string))

        # for showing the Ast



