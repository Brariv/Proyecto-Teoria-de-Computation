def fileReader(filename):
    while True:
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
            break
        except FileNotFoundError:
            print(f"File not found: {filename}")
            filename = input("Enter the path to the text file: ")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            filename = input("Enter the path to the text file: ")
    return [line.strip() for line in lines]


