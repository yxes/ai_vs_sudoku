# ai_vs_sudoku
Deep Dive into Peter Norvig's Sudoku Script

## USAGE

I've never tested this on anything other than python3 so your mileage may vary if you use python 2.7.

### Run

> python sudoku.py

it will ask you for a filename that houses your sudoku problem. The first run you should just use the default and
press enter.

After that you'll want to solve your own problems. The easiest way is just to create your puzzle on Google Drive, download
it as a CSV and store that file in the `./puzzles/` directory.

### Sample Sudoku Puzzle

[Google Drive Puzzle](https://docs.google.com/spreadsheets/d/13wQfoOzZNTflQEwkxsoY4dY4b1QjnfnAvybKxBPr7h0/edit?usp=sharing)

1. Copy the puzzle to your own Google Drive account.
2. Update your copy with your own unsolved puzzle.
3. Save the puzzle as a CSV (File -> Download as -> Comma-separated Values)

Save this file in the `./puzzles/` directory with a unique filename. When you run `sudoku.py` you will be asked for the
filename, enter just the filename (it knows to look for puzzles in the `./puzzles/` directory.)

## TODO

This would be so much cooler if it solved your google drive puzzle by just updating the page. I may get to that.

## Author 

Peter Norvig did ~~most of~~ the work. I inverted rows and columns so they would match the
spreadsheet, used longer and simpler methods in cases where I thought it would read easier, use a
simplier interface (mainly files) for input and just generally make more sense.

[Solving Every Sudoku Puzzle](http://norvig.com/sudoku.html)

Steve Wells <steve@stephendwells.com>

## License

[MIT](http://rem.mit-license.org/)
