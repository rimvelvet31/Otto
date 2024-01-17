import os
import sys
from src import otto

# Register otto file here
FILE_PATH = "test.otto"


if not os.path.isfile(FILE_PATH):
    print(f"File '{FILE_PATH}' does not exist")
    sys.exit()

if not FILE_PATH.endswith(".otto"):
    print(f"File '{FILE_PATH}' is not a valid .otto file")
    sys.exit()


# File is valid
symbol_table = []  # To store lexemes and tokens

with open(FILE_PATH, "r", encoding="utf-8") as file:
    code = file.read()

    tokens = otto.run(f"<{FILE_PATH}>", code)

    for token in tokens:
        lexeme = token.value
        token_type = token.type

        symbol_table.append([lexeme, token_type])

    print(symbol_table)

# Write symbol table to a text file
OUTPUT_FILE = "symbol_table.txt"

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write("LEXEME".ljust(40) + "TOKEN".ljust(40) + "\n")

    for token_pair in symbol_table:
        lexeme = token_pair[0]
        token = token_pair[1]

        output_file.write(lexeme.ljust(40) + token.ljust(40) + "\n")
