import os
import sys
from tabulate import tabulate

from lexical_analyzer.lexer import Lexer
from syntax_analyzer.parser import Parser

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

    # LEXER: Generate list of tokens
    lexer = Lexer(f"<{FILE_PATH}>", code)
    tokens = lexer.tokenize()

    # Extract lexemes & tokens to symbol table
    for token in tokens:
        lexeme = token.value.strip()
        token_type = token.type
        symbol_table.append([lexeme, token_type])

    # PARSER: Generate parse tree
    parser = Parser(tokens)
    ast = parser.otto_progstmt()
    print(ast)

# Write symbol table to output file
OUTPUT_FILE = "symbol_table.txt"

with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
    output_file.write(tabulate(symbol_table, headers=[
                      "LEXEME", "TOKEN"], tablefmt="pretty"))
