# Maze Treasure Hunt

Maze generation and automatic treasure hunt mini-game program.

![image](https://github.com/wawelgreg/maze-treasure-hunt/assets/141285799/b5397426-37f6-416d-8097-abed256fea06)

# Info

- Meant to be run in shell/terminal.
- Uses Python [Curses](https://docs.python.org/3/howto/curses.html).

## Background

### Maze Generator
The maze generator utilizes an iterative version of the recursive backtracker
algorithm, which is a randomized version of the depth-first search algorithm.
Originally deveoloped with recursion, the program would reach max depth of recursion, therefore,
the *maze_generation()* function had to be implemented with a stack.

The steps of the *maze_generation()* function are as follows:
- Start at the initial cell (designated by R_START, C_START)
- Push these coordinates to the stack
  - While length of stack is not empty
      - Pop coordinates from stack
      - For each direction 2 units from the coordinate:
          - If coordinate found is in the maze and WALL exists:
              - Push the previously popped coordinates to stack
              - Bore hole between previous coordinate and new found coordinate
              - Push new found coordinate to stack
              - Break
- Finally, place TREASURE at the bottom right of the matrix

### Treasure Hunt

The maze traversal uses almost the same algorithm as the iterative maze generation method with recursive backtracking, only that in this traversal method, the most recent coordinate isn't saved to the iterative stack, but rather only points where the tunnel/path splits into two or more directions, where the treasure hunter teleports to instantly after reaching a dead end on his recent path.

The steps of the *traverse(m, r, c, l)* function are as follows:
- Set start of the maze hunt at coordinates denoted by parameters (r, c)
- While true
  - Draw maze hunter at the current coordinate
  - Set the maze hunter's location as TAIL (visited)
  - While look index is less than length of look list
    - Increase value of look index
    - If look coordinate out of bounds
      - continue: Next iteration of while loop
    - If look coordinate is a WALL
      - continue
    - If look coordinate was already visited
      - continue
    - If look coordinate is the TREASURE
      - return coordinate of TREASURE
    - Append new coordinate of availabe traversable path to stack
  - If length of stack == 0
    - return None
  - Pop row, col, etc. from stack
- return None

## Usage

To run, call the executable python file *maze_treasure_hunt.py* from the command line:
```
./maze_treasure_hunt.py
```

The constants at the top of *maze_treasure_hunt.py* can be modified as you please:
```
FRAME_SLEEP = 0.01 # how long a frame should last
WIDTH_C = 60 # Centered view width
HEIGHT_C = 30 # Centered view height
WIDTH = 200 # Maze width
HEIGHT = 100 # Maze height
CENTERED = True
WALL = '\xe2'
TAIL = '='
TREASURE = 'T'
```

*FRAME_SLEEP*: float: This number constant corresponds to the wait time between frame. Pretty much a tickrate of sorts. A higher value will result in slower progression of maze generation.
(1 = One second)

*WIDTH_C*: int: This number constant corresponds to the width of the viewing window of the centered view of the maze treasure hunting traversal.

*HEIGHT_C*: int: This number constant corresponds to the height of the viewing window of the centered view of the maze treasure hunting traversal.

*WIDTH*: int: This number constant corresponds to the width of the maze matrix geenrated.

*HEIGTH*: int: This number constant corresponds to the heigth of the maze matrix geenrated.

*CENTERED*: boolean: This boolean value correpsonds to how the visualization of the maze traversal will be displayed.
- True: Centered view: The treasure hunter will be at the center of the screen, being followed by the visualizer.
- False: Static display of the entire maze matrix from the top left corner of the screen all the way down and right to the bottom right corner of the maze. (A maze larger than 100 width and 50 hegiht will most likely be not fully visible on your terminal screen)

*WALL*: char: This character constant corresponds to the walls displayed on the maze matrix.

*TAIL*: char: This character constant corresponds to the coordinates of the maze that the treasure hunter already visited.

*TREASURE*: char: This character constant corresponds to the treasure displayed on the maze matrix that the treasure hunter is in search for.
