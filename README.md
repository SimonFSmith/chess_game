# chess

A two-player chess game using python and pyglet. No computer AI. All rules implemented except "en passant".

## Features
- All rules except "en passant" implemented (castling, promotion, etc.).
- A piece can only be moved if it's a valid move.
- Shows all possible locations a piece can move to.
- Highlights king red when in check.
- you can't move pieces if a game isn't already started
- A new button game to create a game
  - The new button can't be clicked if a game has already started
- A return button to delete last move
- A stop button to stop the current game
  - The stop button can't be clicked if a game has already started
- A save button to save the history of the player moves
  - The save button can't be clicked if a game has already started
- A rules button to show the general rules of the games
- An about button to show different information about the program
- An history that show every move until now

## How to run?
1. Install Python 3.5 or newer if not already installed.
2. In cmd, type:
```cmd
python3 -m pip install pyglet
```
3. Run *main.py*.

## How to play?
1. Click on a piece to show all possible moves.
2. Click on one of the boxes to which the piece can move.
3. Now it's the other's turn.