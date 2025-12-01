# Checkers Game

A fully featured checkers game implementation with GUI, player statistics tracking, a persistent leaderboard system, and customizable visual themes. Built for two-player local gameplay with game state management.

## Table of Contents

- [Code Conventions](#code-conventions)
- [Logic](#logic)
- [Known Bugs/Flaws](#known-bugsflaws)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Operating Instructions](#operating-instructions)
- [Runtime and Performance](#runtime-and-performance)
- [Licensing Information](#licensing-information)

## Code Conventions

### Naming Conventions

- **Variables**: camelCase
- **Functions**: camelCase
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE
- **Global variables**: camelCase

### Code Style

- **Indentation**: 4 spaces
- Classes, methods, and logical blocks separated by blank lines
- Global state managed through Boolean flags
- Single line comments used throughout for section headers and logic explanations
- TODO comments mark areas for future development
- Inline comments explain conditions and game logic

## Logic

### Board Representation

- **Regular piece values**: 
  - `1` (top/red by default)
  - `-1` (bottom/black by default)
- **King piece values**: 
  - `5` (top/red king)
  - `-5` (bottom/black king)
- **Potential move values**: `99` (grey indicator pieces)
- **Empty squares**: value of `None`
- The visual board is updated each frame based on the condition of the logical array

### Coordinate System

- **Board Array**: `board[row][col]`
  - Row has a range 0-7 (top to bottom on screen)
  - Column has a range 0-7 (left to right on screen)
- **Screen coordinates**: Converted from pixel position to array location
  - This is done via the `returnClickedPiece(pos, board)` function
- **Piece locations**: Stored as tuples, i.e., `(row, col)`
- **Screen dimensions**: 800px wide and 600px high
- **Board dimensions**: (50px, 50px), (450px, 450px)
  - Each space has a dimension of 50px by 50px

### Game Flow Logic

#### Move Calculation (`getPossibleMoves()`)

- Returns a list of potential moves that are legal and in-bounds
- Checks piece type (regular vs king) and color
- **Regular pieces**: Move forward diagonally only
- **King pieces**: Move in all four diagonal directions
- **Jump detection**: If adjacent diagonal has enemy piece and space beyond is empty, jump is valid
- **Multi-jump enforcement**: If jump_piece parameter is set, only jump moves are returned

#### Move Execution

- Validates and executes piece movement
- Handles captures by detecting 2-square diagonal moves (jumps)
- Calculates captured piece position: `location + (destination - location) / 2`
- Promotes pieces to kings when reaching the opposite end
- Updates piece object location and board array

#### Win Condition (`checkWin()`)

- Iterates through all pieces on board
- Counts pieces with available legal moves for each color
- Win declared when one color has zero pieces with legal moves
- Updates `player1Win` or `player2Win` global flags

#### Turn Management

- Turn tracked with integer: `1` for red/top player, `-1` for black/bottom player
  - Same convention as piece values for simplicity
- Turn multiplied by -1 to switch: `turn *= -1`
- **Double jump exception**: Turn doesn't switch until all jumps completed
- `double_jump` variable stores piece that must continue jumping

#### State Management

- Game uses boolean flags for screen states:
  - `displayStart`, `displayInput`, `displayBoard`, `displaySettings`, `displayEnd`, `displayLeaderboard`
- Only one display state active at a time
- Event handlers check active state before processing inputs

## Known Bugs/Flaws

1. **File Error Handling**
   - No try-catch around accessing assets
   - Potentially, the program can crash if files are corrupted
   - Recommend implementing file error handling

2. **Leaderboard File Locking**
   - If Excel file is open in another program during game end, save operation fails
   - Leaderboard updates are lost
   - Recommend add error handling if workbook is already open

3. **Player Name Input Validation**
   - Currently player names accept any string including unprintable characters
   - This can lead to visual bugs or strings that Excel cannot handle
   - Recommend adding name input validation

## Dependencies

- Python >= 3.13
- Pip package manager
- numpy >= 2.3.5
- pygame >= 2.6.1
- openpyxl >= 3.1.0
- sys (standard library)
- os (standard library)
- operator (standard library)

## Installation

### CLI Steps

**Prerequisites:**
1. Python version 3.13
2. Pip package manager
3. Git

**Commands:**

```bash
git clone https://github.com/lmfenicle/Checkers-Project.git
cd Checkers-Project
python -m venv venv
venv/Scripts/activate
pip install openpyxl numpy pygame
cd Checkers_Game
python checkers.py
```

### Alternative IDE Method

**Prerequisites:**
1. Python Interpreter or IDE such as PyCharm
2. Python version 3.13

**Steps:**
1. Download the repository from https://github.com/lmfenicle/Checkers-Project.git
2. Open the folder and navigate to `Checkers-Project/Checkers_Game`
3. Open `Checkers.py` with your IDE
4. In the IDE terminal, type the command `pip install openpyxl numpy pygame`
5. Finally, run the program

## Operating Instructions

### Startup

1. **Start Screen**: Press ENTER to continue
2. **Name Input Screen**:
   - Enter Player 1 name (max 10 characters)
   - Press ENTER
   - Enter Player 2 name (max 10 characters)
   - Press ENTER
3. Game Board Appears with Player 1's turn

### Gameplay Controls

1. Click on one of your pieces (current turn is displayed on screen)
2. Grey circles appear showing all valid moves
   - If no grey circles appear, there is no valid move. Click on another piece
3. Click on a grey circle to move your piece
4. If you jump over a piece to capture it, you capture another piece if available
   - If you cannot capture another piece, your turn is over
   - If you do not want to capture another piece, click outside of the board to end your turn
5. If a piece reaches the opposite end of the board, that piece automatically becomes a king and may move in all 4 directions if permitted
   - King pieces are denoted by a star on the piece
6. Both players take turns until one player has no more valid moves, thus the other player wins
7. Once a player wins, their name will be displayed on screen
8. From there, the players may choose to play again or quit

### Settings Menu

- Settings Menu is located at the top right corner of the screen
- From here the player can cycle through the different color pallets
  - The current theme will be displayed
- In the Menu, below the theme selection, there are the surrender buttons
  - Players must click the surrender button twice to officially surrender
- Below the surrender buttons, there is the toggle stats checkbox
  - Players may toggle this to show/hide the current stats

### Leaderboard Screen

- Leaderboard display button is located on the left of the settings menu
- Displays the current leaderboard statistics
- The sort button toggles the sorting between wins, losses, and win ratio

## Runtime and Performance

### Operational Times

- **Cold start**: ~1-2 seconds
- **PyGame initialization**: ~0.5 seconds
- **Leaderboard loading**: ~0.1 seconds (may depend on file size)
- **Frame Rate**: capped at 60fps
- **Move calculation**: <1ms per piece
- **Board rendering**: ~2-5ms per frame
- **Excel leaderboard update**: ~50-100ms at game end
- **Win condition**: ~1ms every frame

### Memory Usage

- Typically 50-80 MB
- NumPy array overhead: 10-20 MB
- File size: ~30 KB
  - Leaderboard.xlsx: ~8-12 KB (grows over time)

## Licensing Information

### MIT License

Copyright (c) 2025 Lance Fenicle & Jack Meadows

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Usage Rights

**Permitted:**
- Commercial use
- Distribution
- Modification
- Private use

**Conditions:**
- License and copyright notice condition
- A copy of the license must be included with the licensed material

**Limitations:**
- Limitation of liability
- Does not provide any warranty

### Third-Party Dependencies

- **NumPy** ([BSD 3-Clause License](https://numpy.org/doc/stable/license.html)) - Free to use
- **Pygame** ([LGPL License](https://www.pygame.org/docs/LGPL.txt)) - Free to use
- **Openpyxl** ([MIT License](https://openpyxl.readthedocs.io/en/stable/#license)) - Permissive license allowing commercial use
- **Python** ([PSF License](https://www.python.org/doc/copyright/)) - GPL-compatible open-source license, free to use
