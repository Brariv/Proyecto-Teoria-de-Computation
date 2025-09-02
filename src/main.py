from drawing.nfa import nfaToDiGraph
from match.nfa_match import matchStringToNfa
from parsing.dfa import nfaToDfa
from parsing.nfa import postfixToNfa
from parsing.postfix import infixToPostfix
from utils.argument_parsing import parseLexerArgs
from utils.file_parsing import fileReader


if __name__ == "__main__":

    parse_arguments = parseLexerArgs();

    lines:list[str] = fileReader(parse_arguments.regex_file); 

    for line in lines:
        postfix = infixToPostfix(line)

        nfa = postfixToNfa(postfix)

        # For showing the nfa
        if matchStringToNfa(nfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, is part of the regex : {line}")
        else:
            print(f"The string: {parse_arguments.string}, is not part of the regex : {line}")

        nfaToDiGraph(nfa).render(f"nfa_imgs/nfa_from_{line}", format="png", cleanup=True) # To lazy for having the count, just making a random tree

        # For showing the dfa

        if __debug__:
            dfa = nfaToDfa(nfa)

            nfaToDiGraph(nfa).render(f"dfa_imgs/nfa_from_{line}", format="png", cleanup=True)



