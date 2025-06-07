Tic-Tac-Toe Game with Tkinter GUI
This project implements a Tic-Tac-Toe game with a graphical user interface using Python's Tkinter library. The game features a player (O) versus an AI opponent (X), with a clean, modern interface and strategic AI gameplay.
Features

3×3 Game Board: A grid of buttons for gameplay.
Score Tracking: Displays scores for Player (O), AI (X), and draws.
Modern Interface: Dark blue background with color-coded elements.
Strategic AI: Plays optimally but fairly, prioritizing winning moves, blocking, and strategic positioning.

Class Structure

TicTacToeGUI: A single class handling game logic, UI setup, and AI behavior.

Initialization

Creates a 500×600 pixel window with a dark blue background.
Initializes a 9-space game board (list of blank spaces).
Configures fonts for UI elements.
Sets up:
Title label.
Score display (AI: X, Player: O, Draws).
3×3 grid of clickable buttons.
Status label for game state updates.
Control buttons (start/end game).


AI makes the first move.

Game Logic

Follows standard Tic-Tac-Toe rules:
Players alternate placing X (AI) or O (Player) on empty squares.
Win condition: Three tokens in a row (horizontal, vertical, or diagonal).
Draw condition: All squares filled without a winner.



AI Logic
The AI employs a strategic approach:

Checks for immediate winning move.
Blocks player's potential winning move.
Prioritizes strategic moves:
Takes the center if available.
Sets up potential winning patterns.
Chooses corner squares for advantage.
Falls back to side squares or random moves if no strategic option exists.



Game Flow

AI starts (typically center or corner).
Player clicks an empty square to place O.
After each move:
Game checks for a winner.
If won, highlights winning line and updates score.
If board is full without a winner, declares a draw.


Players can start a new game at any time via control buttons.

Requirements

Python 3.x
Tkinter (included with standard Python installation)

Usage

Run the Python script.
AI (X) makes the first move.
Click an empty square to place O.
Use the "New Game" button to reset or start over.

Pros

Intuitive, user-friendly interface.
Strategic AI ensures challenging yet fair gameplay.
Lightweight and easy to run.

Cons

Limited to 3×3 grid (no support for larger boards).
AI is deterministic in some scenarios, which may feel predictable.

