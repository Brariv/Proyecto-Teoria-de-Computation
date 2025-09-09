from drawing.nfa import nfaToDiGraph
from drawing.dfa import dfaToDiGraph
from match.nfa_match import matchStringToNfa
from match.dfa_match import matchStringToDfa
from parsing.dfa import  nfaToDfa
from parsing.min_dfa import minimizeDfa
from parsing.nfa import postfixToNfa
from parsing.postfix import infixToPostfix
from utils.argument_parsing import parseLexerArgs
from utils.character_parsing import regexToStandarizeRegex
from utils.file_parsing import fileReader


if __name__ == "__main__":

    parse_arguments = parseLexerArgs();

    lines:list[str] = fileReader(parse_arguments.regex_file); 

    for line in lines:
        line = regexToStandarizeRegex(line) # in case of any weird characters that ccan also be consider valid in a regex

        postfix = infixToPostfix(line)

        nfa = postfixToNfa(postfix)

        dfa = nfaToDfa(nfa)

        nfaToDiGraph(nfa).render(f"files/nfa_imgs/nfa_from_{line}", format="png", cleanup=True) # overriding the last one, so yeah

        # before we mutate the dfa for minimization
        dfaToDiGraph(dfa).render(f"files/dfa_imgs/dfa_from_{line}", format="png", cleanup=True)  # overriding the last one, so yeah

        # we start looking for matching
        print(f"\nGoing through regex: {line}\n")

        print("DFA Matching:")

        if matchStringToDfa(dfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the DFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the DFA")


        print("NFA Matching:")

        if matchStringToNfa(nfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the NFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the NFA")

        min_dfa = minimizeDfa(dfa) # the minimization
        # we render the min dfa
        dfaToDiGraph(min_dfa).render(f"files/min_dfa_imgs/min_dfa_from_{line}", format="png", cleanup=True)  # overriding the last one, so yeah

        print("MIN-DFA Matching:")

        if matchStringToDfa(min_dfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the MIN-DFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the MIN-DFA")






