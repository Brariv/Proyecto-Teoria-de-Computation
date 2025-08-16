from match.dfa_match import matchStringToRegex
from parsing.ast import postfixToAst
from parsing.postfix import infixToPostfix
from utils.file_parsing import fileReader


if __name__ == "__main__":
    filename:str = "files/regex.txt" 
    lines:list[str] = fileReader(filename) 

    for line in lines:
        postfix = infixToPostfix(line)

        # Just for looking how the Nfa should look

        ast = postfixToAst(postfix)

        print(matchStringToRegex(postfix, "a"))

        # for showing the Ast



