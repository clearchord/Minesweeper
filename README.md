# Minesweeper Solver

This program generates and solves Minesweeper problems.

A problem is to be saved in a problem file whose format is given as below.

<pre>
10 10 # The height and width of a board.
0 0   # The position of an initial cell which is randomly selected and luckily has no neighbor mine.
12    # The number of mines embedded on the board.
0 7   # The position of a cell with a mine for each remaining line.
1 2
1 6
2 3
3 2
5 3
5 5
5 8
6 0
6 9
8 2
9 4
</pre>

Usage:

To generate a problem, 

`python Minesweeper.py generate path_to_problem_file height width mine_ratio`

To solve a problem, 

`python Minesweeper.py solve path_to_problem_file`

The algorithm is not quite enough and needs to be refined.

Anyway, enjoy sweeping!
