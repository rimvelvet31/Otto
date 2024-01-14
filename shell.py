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
    lines = file.readlines()

for line in lines:
    line = line.strip()
    tokens = otto.run(f"<{FILE_PATH}>", line)

    for token in tokens:
        lexeme = token.value
        token_type = token.type
        symbol_table.append((lexeme.ljust(40), token_type.ljust(40)))

# Write symbol table to a text file
OUTPUT_FILE = "symbol_table.txt"

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write("LEXEME".ljust(40) + "TOKEN".ljust(40) + "\n")

    for lexeme, token_type in symbol_table:
        output_file.write(f"{lexeme}{token_type}\n")
