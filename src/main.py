from drawing.nfa import nfaToDiGraph
from drawing.dfa import dfaToDiGraph
from match.nfa_match import matchStringToNfa
from match.dfa_match import matchStringToDfa
from parsing.dfa import  nfaToDfa
from parsing.min_dfa import minimize_dfa
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

        dfa = nfaToDfa(nfa)

        nfaToDiGraph(nfa).render(f"nfa_imgs/nfa_from_{line}", format="png", cleanup=True) # overriding the last one, so yeah

        dfaToDiGraph(dfa).render(f"dfa_imgs/dfa_from_{line}", format="png", cleanup=True)  # overriding the last one, so yeah

        print(f"\nGoing through regex: {line}")

        print("DFA Matching")

        if matchStringToDfa(dfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the DFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the DFA")


        print("NFA Matching")

        if matchStringToNfa(nfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the NFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the NFA")



        dfa = minimize_dfa(dfa)


        dfaToDiGraph(dfa).render(f"min_dfa_imgs/min_dfa_from_{line}", format="png", cleanup=True)  # overriding the last one, so yeah


        print("\nMIN-DFA Matching")

        if matchStringToDfa(dfa, parse_arguments.string):
            print(f"The string: {parse_arguments.string}, did match the MIN-DFA")
        else:
            print(f"The string: {parse_arguments.string}, didn't match the MIN-DFA")







