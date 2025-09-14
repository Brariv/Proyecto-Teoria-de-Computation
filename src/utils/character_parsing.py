
#TODO: add more equivalence classes
import re


eq_classes:dict[str,str] = {
    "a-z":"a|b|c|d|e|f|g|h|i|j|k|l|m|o|p|q|r|s|t|u|v|w|x|y|z",
    "A-Z":"A|B|C|D|E|F|G|H|I|J|K|L|M|O|P|Q|R|S|T|U|V|W|X|Y|Z",
    "0-9":"0|1|2|3|4|5|6|7|8|9"

}

# given a equivalence class, it returns the shunting yard's friendly string
# Given the form of the class [<the representative of the class>]
def _equivalenceClassToString(eq_class:str)->str:

    # compose of the characters of the equivalnce-class operate it with a |
    representation_eq_class:str = str()

    # eq_class without  "[" and "]"
    parsed_eq_class:str = eq_class.replace("[","").replace("]","")

    # we will be concatenating to this string, and searching in the dict for a value.
    # in the case we find a value, we reset it and repeat the process
    actual_eq_class:str = str()

    # we iterate of the equivalnce-class to see each representative
    for char in parsed_eq_class:
        
        # we put a value in to it
        actual_eq_class+=char

        if eq_classes.get(actual_eq_class, None):
            #we add the or operator in case of new ones
            representation_eq_class += (eq_classes[actual_eq_class] + "|")
            # and we reset it for checking new ones
            actual_eq_class = str()

    # and then we return the representation with a more friendly form
    return "(" + representation_eq_class[0:len(representation_eq_class)-1] + ")" # I ain't returning all of it, cause of the "|" will always be the final operator


# given a regex with common operators and equivalence-classes, returns that same regex with parse operators
def regexToStandarizeRegex(regex:str)->str:
    new_regex:str = regex
    for ch_idx in range(len(regex)):
        # wanted to made a more fancy solution, but that implies to refactor a lot of that
        # code base, and I'm not in the mood of doing it
        match regex[ch_idx]:
            case "*":
                new_regex = new_regex.replace("*", "∗")
            case "[":
                eq_class = str()

                temp_ch_idx:int = ch_idx
                while regex[temp_ch_idx] != "]":
                    eq_class += regex[temp_ch_idx]
                    temp_ch_idx += 1

                new_regex = new_regex.replace(eq_class + "]", _equivalenceClassToString(eq_class + "]"))
            case _:
                pass

    return new_regex

