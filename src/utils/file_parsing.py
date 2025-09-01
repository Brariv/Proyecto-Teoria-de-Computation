def fileReader(filename:str) -> list[str]:
    while True:
        try:
            with open(filename, "r") as file:
                lines:list[str] = file.readlines()
            break
        except FileNotFoundError:
            print(f"File not found: {filename}")
    return [line.strip() for line in lines]

