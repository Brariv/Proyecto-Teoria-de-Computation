# given a regex with common operators, returns that same regex with parse operators
def regexToStandarizeRegex(regex:str)->str:
    new_regex = str()
    for ch in regex:
        # wanted to made a more fancy solution, but that implies to refactor a lot of that
        # code base, and I'm not in the mood of doing it
        match ch:
            case "*":
                new_regex+="∗"
            case _:
                new_regex+=ch
    return new_regex

