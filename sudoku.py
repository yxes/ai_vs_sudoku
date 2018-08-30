#!/usr/bin/python

"""
DEFINITIONS
"""
label_cols = 'ABCDEFGHI'
label_rows = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

cells = cross(label_cols, label_rows)

rows = [cross(label_cols, r) for r in label_rows]
columns = [cross(c, label_rows) for c in label_cols]
squares = [
  cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')
]

megalist = rows + columns + squares

# { cell: [ [row], [col], [square] ] }
influencers = dict((s, [u for u in megalist if s in u]) for s in cells)

# { cell: { set of unique influencers } }
peers = dict((s, set(sum(influencers[s],[]))-set([s])) for s in cells)


def display(values, empty=False):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    if empty:
        values = dict([ (v, '.' if values[v] == '123456789' else values[v]) for v in values ])

    width = 1+max(len(values[s]) for s in cells)
    line = '+'.join(['-'*(width*3)]*3)

    for c in label_cols:
        print(''.join(values[c+r].center(width)+('|' if r in '36' else '')
                      for r in label_rows))
        if c in 'CF': print(line)
    return

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The cells, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(cells, chars))
    
def eliminate(values):
    """
    Go through all the cells, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in megalist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
          [ box for box in values.keys() if len(values[box]) == 1 ]
        )
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len(
          [box for box in values.keys() if len(values[box]) == 1]
        )
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier

    if all(len(values[s]) == 1 for s in cells): 
        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in cells if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    print("input grid\n")
    values = grid_values(grid)
    display(values, True)

    print("\nsolved grid\n")
    display(search(values))
    print("\n\n")

def create_grid(filename):
    grid = str()
    with open('puzzles/' + filename, 'r') as f:
        grid = ''.join(
          [ '.' if x == '' else x 
              for row in f.readlines() 
                for x in row.strip().split(',')
          ]
        )

    if grid is None:
        print("filename: {} is empty...".format(filename))

    return grid   

if __name__ == "__main__":

    #grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

    #grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    #solve(grid)
    #solve(grid2)

    filename = input("enter the filename of your sudoku puzzle [sudoku.csv]: ")
    if filename == '':
        filename = 'sudoku.csv'
    grid = create_grid(filename)
    solve(grid)
