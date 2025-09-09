# Python-Multi-Automata-Lexer

A full circle lexer's implementation made purely with python utilities (except for the imgs).

## How to use:

### Using Nix Flakes (recommended):
  - Use the nix develop command:
    ```fish
      nix develop . --command "python3" "-O" "src/main.py" "<desire path>" "files/regex.txt" "--string" "<desire string>"
    ```

### Using Python venv:
  - Setup venv first:
      ```fish
      python3 -m venv. 
      ```
  - Activate enviroment (doing it for fish):
      ```fish
      source bin/activate.fish
      ```
  - Download needed dependencies:
    ```fish
      python3 -m pip install -r requirements.txt
      ```
  - Run script with desire arguments:
      ```fish
      python3 -O src/main.py --regex_file "<desire path>" "--string" "<string you want to try out>"
      ```

### Using Python global enviroment:
  - Install the requirements.txt:
      ```fish
      python3 -m pip install -r requirements.txt
      ```
  - Run script with desire arguments:
      ```fish
      python3 -O src/main.py --regex_file "<desire path>" "--string" "<string you want to try out>"
      ```



# Demostration Video:
[Demostration video](https://youtu.be/15SS0grseTE) 
