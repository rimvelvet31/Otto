import os
import sys
from tabulate import tabulate
from src import otto

# Register otto file here
FILE_PATH = "test.otto"


if not os.path.isfile(FILE_PATH):
    sys.exit(f"ERROR: File '{FILE_PATH}' does not exist")

if not FILE_PATH.endswith(".otto"):
    sys.exit(f"ERROR: File '{FILE_PATH}' is not a valid .otto file")


# File is valid
symbol_table = []  # To store lexemes and tokens

# Process and scan file for tokens
with open(FILE_PATH, "r", encoding="utf-8") as file:
    code = file.read()

    # Generate list of Token objects with attributes: type, value
    tokens = otto.run(f"<{FILE_PATH}>", code)

    # Extract lexemes and tokens
    for token in tokens:
        lexeme = token.value.strip()
        token_type = token.type

        symbol_table.append([lexeme, token_type])


OUTPUT_FILE = "symbol_table.txt"

# Write symbol table to output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write(tabulate(symbol_table, headers=[
                      "LEXEME", "TOKEN"], tablefmt="pretty"))
