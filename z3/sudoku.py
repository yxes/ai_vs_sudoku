#!/usr/bin/env python

from z3 import *
from itertools import chain  # flatten nested lists; chain(*[[a, b], [c, d], ...]) == [a, b, c, d, ...]
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [[Int("{}{}".format(r, c)) for c in cols] for r in rows]  # declare variables for each box in the puzzle
s_solver = Solver()  # create a solver instance

# Add constraints that every box has a value between 1-9 (inclusive)
s_solver.add( *chain(*[(1 <= b, b <= 9) for b in chain(*boxes)]) )

# Add constraints that every box in a row has a distinct value
s_solver.add( *[Distinct(r) for r in boxes] )

# Add constraints that every box in a column has a distinct value
s_solver.add( *[Distinct(col) for col in zip(*boxes)] )

# Add constraints so that every box in a 3x3 block has a distinct value
s_solver.add( *[Distinct([boxes[i + ii][j + jj] for ii in range(3) for jj in range(3)]) for j in range(0, 9, 3) for i in range(0, 9, 3)] )

# use the value 0 to indicate that a box does not have an assigned value
#board = ((0, 0, 3, 0, 2, 0, 6, 0, 0),
#         (9, 0, 0, 3, 0, 5, 0, 0, 1),
#         (0, 0, 1, 8, 0, 6, 4, 0, 0),
#         (0, 0, 8, 1, 0, 2, 9, 0, 0),
#         (7, 0, 0, 0, 0, 0, 0, 0, 8),
#         (0, 0, 6, 7, 0, 8, 2, 0, 0),
#         (0, 0, 2, 6, 0, 9, 5, 0, 0),
#         (8, 0, 0, 2, 0, 3, 0, 0, 9),
#         (0, 0, 5, 0, 1, 0, 3, 0, 0))

board = ((8, 0, 0, 0, 0, 0, 0, 0, 0),
         (0, 0, 3, 6, 0, 0, 0, 0, 0),
         (0, 7, 0, 0, 9, 0, 2, 0, 0),
         (0, 5, 0, 0, 0, 7, 0, 0, 0),
         (0, 0, 0, 0, 4, 5, 7, 0, 0),
         (0, 0, 0, 1, 0, 0, 0, 3, 0),
         (0, 0, 1, 0, 0, 0, 0, 6, 8),
         (0, 0, 8, 5, 0, 0, 0, 1, 0),
         (0, 9, 0, 0, 0, 0, 4, 0, 0))

# Add constraints boxes[i][j] == board[i][j] for each box where board[i][j] != 0
s_solver.add( *[boxes[i][j] == board[i][j] for i in range(9) for j in range(9) if board[i][j] != 0] )

assert s_solver.check() == sat, "Uh oh. The solver didn't find a solution. Check your constraints."
for row, _boxes in enumerate(boxes):
    if row and row % 3 == 0:
        print('-'*9+"|"+'-'*9+"|"+'-'*9)
    for col, box in enumerate(_boxes):
        if col and col % 3 == 0:
            print('|', end='')
        print(' {} '.format(s_solver.model()[box]), end='')
    print()
