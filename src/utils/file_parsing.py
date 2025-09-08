def fileReader(filename:str) -> list[str]:
    while True:
        try:
            with open(filename, "r") as file:
                lines:list[str] = file.readlines()
            break
        except FileNotFoundError:
            print(f"File not found: {filename}")
            exit(1) # if the file ain't found, why will need to loop and expect for it
    return [line.strip() for line in lines if line != "\n"] # doing safe check for not introducing empty strings to the lexer

