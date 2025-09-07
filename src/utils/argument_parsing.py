from argparse import ArgumentParser, Namespace

# function for getting arguments from cli
def parseLexerArgs() -> Namespace:
    parser = ArgumentParser()
    
    # I don't want to input my string, this flow is cleaner, like DUH
    parser.add_argument("--regex_file", dest="regex_file", type=str, help="Add the regex file")
    parser.add_argument("--string", dest="string", type=str, help="Add the string")

    parse_args = parser.parse_args()

    if parse_args.regex_file is None or parse_args.string is None:
        raise Exception("Arguments where not suplly")

    return parse_args




