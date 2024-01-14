# Otto

Enter Otto, a high-level and dynamic programming language geared towards **automation**. Our goal is to make automating tasks an experience that is convenient and accessible for both professionals and enthusiasts seeking to automate mundane tasks. With Otto taking care of the monotonous processes, users can streamline their workflow to focus more on the core logic and ideas behind their programs.

# Instructions

- To view the lexer files, go to the `src` folder, where you can find:
  - `otto.py`, where the lexer logic is located
  - `constants.py`, where token types are defined in
  - `error.py`, a class for handling errors
  - `position.py`, a class for tracking the position of each character scanned
- To run the lexer, either:
  - open your terminal and run the command `python shell.py` (make sure you're in the root directory!)
  - use the built-in ▶️ Run button/feature on your IDE
- To write your own otto code to be scanned by the lexer, go to `test.otto`
- To see the output, go to `symbol_table.txt`, which contains the table of lexemes and tokens
