# Otto

Enter Otto, a high-level and dynamic programming language geared towards **automation**. Our goal is to make automating tasks an experience that is convenient and accessible for both professionals and enthusiasts seeking to automate mundane tasks. With Otto taking care of the monotonous processes, users can streamline their workflow to focus more on the core logic and ideas behind their programs.

# Folder Structure

- ## lexer
  - `constants.py`, where token types are defined in
  - `lexer.py`, where the lexer logic is located in
  - `position.py`, used to track the position of scanned characters
  - `regex.py`, which contains regex for identifying some tokens
- ## syntax_analyzer
  - `nodes.py`, where nodes of the parse tree are located
  - `parse_result`, this temporarily stores tokens to be parsed until the parser returns a successful or failed parsing
  - `parser.py`, where the main parsing logic is located in
- ## utils
  - contains utility functions (mostly error handling)
- ## `main.py`
  - Entry point of the program (this is the file to run)

# Instructions to run

1. Recommended to set up a venv first
   - Run `python -m venv venv`
   - Activate `./venv/Scripts/activate`
2. Install dependencies
   - Run `pip install -r requirements.txt`
3. Edit Otto code to test in `test.otto`
4. Run `main.py`
5. View the lexer output in `symbol_tree.txt`
6. View the parser output in `parse_tree.txt`
